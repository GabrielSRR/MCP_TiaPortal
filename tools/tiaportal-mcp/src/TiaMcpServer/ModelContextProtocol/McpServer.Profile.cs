using ModelContextProtocol.Server;
using System;
using System.Collections.Generic;
using System.Reflection;

namespace TiaMcpServer.ModelContextProtocol
{
    // TIA_MCP_PROFILE=lite: expose only the ~42 essential tools instead of ~200, so a
    // small / non-expert model is not drowned in choices and hosts with a tool cap
    // (VS Code: 128) can enable everything. `tia config` writes the lite profile by
    // default since v2.3.1 (pass --full for the whole tool surface); the server-side
    // default without the env var remains full. All tools are static so no DI target
    // is needed.
    public static partial class McpServer
    {
        // Explicit allowlist (tool Name, not method name). Kept explicit on purpose:
        // membership must not silently change when a [Lx] description prefix is edited.
        // = all [L0]/[L1] tools + the golden-path tools ServerInstructions/GetAuthoringGuide
        // tell the model to call (previously [L2] and thus missing from lite — a weak
        // model in lite was instructed to call ImportFromDocuments and couldn't see it).
        private static readonly HashSet<string> LiteToolNames = new HashSet<string>(StringComparer.Ordinal)
        {
            // L0 — orientation / diagnostics
            "Bootstrap", "Doctor", "GetState", "GetAuthoringGuide",
            "GenerateAcceptanceReport", "GenerateErrorReport",
            "RunCapabilitySelfTest", "RunOnlineMonitoringSafetySelfTest",
            // L1 — session / project lifecycle
            "Connect", "Disconnect", "ListPortalProcessProjects", "EnsureOpennessUserGroup",
            "OpenProject", "AttachToOpenProject", "CreateProject", "SaveProject", "CloseProject",
            "GetProject", "GetProjectTree", "ValidateAutomationContext",
            // L1 — read / understand
            "GetSoftwareInfo", "GetSoftwareTree", "GetDevices", "DescribeBlockLogic",
            // L1 — build / import / compile
            "ScaffoldProject", "PlcBuildAndImport", "ImportBlock", "ImportType",
            "ImportPlcTagTable", "WritePlcSclSourceFile",
            "CompileSoftware", "CompileAndDiagnosePlc",
            // L1 — hardware
            "AddDeviceWithFallback", "SearchHardwareCatalog", "ConnectDeviceNodesToProfinetSubnet",
            // Golden-path tools referenced by ServerInstructions / GetAuthoringGuide
            // (previously [L2]; without them the lite roster contradicts the instructions)
            "ImportFromDocuments", "GenerateBlocksFromExternalSource",
            // Batch SD import/export are the "PREFERRED on V21+" batch path in the same
            // instructions; tag tables and cross-references are what a model needs to read a
            // project it did not write.
            "ImportBlocksFromDocuments", "ExportBlocksAsDocuments",
            "GetPlcTagTables", "GetCrossReferences",
            "GetBlocks", "GetBlocksWithHierarchy", "GetBlockInfo",
            "ExportAsDocuments", "GoOffline",
        };

        public static IList<McpServerTool> GetLiteTools()
        {
            var tools = new List<McpServerTool>();
            foreach (var method in typeof(McpServer).GetMethods(BindingFlags.Public | BindingFlags.Static))
            {
                var attr = method.GetCustomAttribute<McpServerToolAttribute>();
                if (attr == null) continue;
                var name = attr.Name ?? method.Name;
                if (LiteToolNames.Contains(name))
                {
                    tools.Add(McpServerTool.Create(method));
                }
            }
            return tools;
        }

        public static bool IsLiteProfile()
        {
            return string.Equals(
                Environment.GetEnvironmentVariable("TIA_MCP_PROFILE")?.Trim(),
                "lite", StringComparison.OrdinalIgnoreCase);
        }
    }
}
