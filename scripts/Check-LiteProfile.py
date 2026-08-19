# -*- coding: utf-8 -*-
"""Assert that TIA_MCP_PROFILE=lite is still a USABLE profile.

lite is what 配置MCP.bat --lite writes for weak models and tool-capped hosts (VS Code caps at
128). It is only worth recommending if a model restricted to it can still walk the golden path
end to end. It could not: ImportFromDocuments / ExportAsDocuments / GetBlocks / GetBlockInfo /
GetCrossReferences were all [L2], so a lite session could open a project and see the tree but
could neither list a block nor use the PREFERRED document import path. Nothing caught that,
because nothing checked it. This does.

Usage:  python scripts/Check-LiteProfile.py [path-to-TiaMcpServer.exe]
Exit 0 = lite is self-sufficient and fits the host cap.
"""
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "runtime" / "v21" / "TiaMcpServer.exe"

# The documented golden path: orientation -> connect/open -> read -> author -> compile -> save.
# Every name here is referenced by the server instructions, README or GetAuthoringGuide, so a
# profile that omits one is advertising a workflow it cannot perform.
REQUIRED = [
    # orientation / diagnostics
    "Bootstrap", "Doctor", "GetAuthoringGuide", "GetState",
    # session + project
    "Connect", "Disconnect", "OpenProject", "CreateProject", "AttachToOpenProject",
    "CloseProject", "SaveProject", "GetProject", "GetProjectTree", "GetSoftwareTree",
    # read / understand
    "GetBlocks", "GetBlocksWithHierarchy", "GetBlockInfo", "DescribeBlockLogic",
    "GetCrossReferences", "GetPlcTagTables",
    # author (golden path: SD documents preferred, SCL external source alternative)
    "ScaffoldProject", "PlcBuildAndImport", "WritePlcSclSourceFile",
    "ImportFromDocuments", "ExportAsDocuments",
    "ImportBlocksFromDocuments", "ExportBlocksAsDocuments",
    "GenerateBlocksFromExternalSource",
    # verify
    "CompileSoftware", "CompileAndDiagnosePlc",
]

# VS Code refuses to enable more tools than this; lite exists to stay under it.
HOST_TOOL_CAP = 128


def tools_for_profile(profile):
    env = dict(os.environ)
    if profile:
        env["TIA_MCP_PROFILE"] = profile
    else:
        env.pop("TIA_MCP_PROFILE", None)
    p = subprocess.Popen([str(EXE), "--logging", "0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
                         bufsize=1, env=env)
    seq = [0]

    def send(method, params=None, notify=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not notify:
            seq[0] += 1
            msg["id"] = seq[0]
        p.stdin.write(json.dumps(msg) + "\n")
        p.stdin.flush()
        if notify:
            return None
        while True:
            line = p.stdout.readline()
            if not line:
                raise SystemExit("engine closed stdout:\n" + p.stderr.read())
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("id") == seq[0]:
                return d

    try:
        send("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                            "clientInfo": {"name": "lite-check", "version": "1"}})
        send("notifications/initialized", {}, notify=True)
        return [t["name"] for t in send("tools/list", {})["result"]["tools"]]
    finally:
        try:
            p.stdin.close()
        except Exception:
            pass
        p.terminate()


def main():
    if not EXE.exists():
        print("[FAIL] engine not found:", EXE)
        return 1
    print("engine:", EXE)

    full = tools_for_profile(None)
    lite = tools_for_profile("lite")
    print("full profile: %d tools" % len(full))
    print("lite profile: %d tools" % len(lite))

    failures = []
    missing = [n for n in REQUIRED if n not in lite]
    if missing:
        failures.append("lite is missing golden-path tools: " + ", ".join(missing))

    unknown = [n for n in REQUIRED if n not in full]
    if unknown:
        failures.append("REQUIRED lists tools this engine does not expose at all: " + ", ".join(unknown))

    if len(lite) > HOST_TOOL_CAP:
        failures.append("lite exposes %d tools, over the %d host cap it exists to respect"
                        % (len(lite), HOST_TOOL_CAP))

    if not lite:
        failures.append("lite exposed no tools")

    for f in failures:
        print("[FAIL]", f)
    if failures:
        return 1
    print("[ ok ] lite covers all %d golden-path tools and stays under the %d cap"
          % (len(REQUIRED), HOST_TOOL_CAP))
    return 0


if __name__ == "__main__":
    sys.exit(main())
