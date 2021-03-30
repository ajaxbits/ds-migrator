initial_antimalwareconfig = ["0", "4", "1", "2", "3"]
initial_directorylist = ["1"]
initial_fileextensionlist = ["2"]
initial_filelist = ["1", "2"]
initial_allamconfignew = ["241", "242", "243", "244"]
test_allamconfigdict = {0: 0, 4: 241, 1: 242, 2: 243, 3: 244}
initial_amalldirectorynew = ["131"]
initial_amallfileextensionnew = ["93"]
initial_amallfilelistnew = ["168", "169"]
test_json = '{"name":"Advanced Real-Time Scan Configuration"}'
t1getallamconfig = [
    '{"name":"Advanced Real-Time Scan Configuration","description":"","scanType":"real-time","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-and-heuristic","documentExploitHeuristicLevel":"default-and-agressive","machineLearningEnabled":true,"behaviorMonitoringEnabled":true,"documentRecoveryEnabled":true,"intelliTrapEnabled":true,"memoryScanEnabled":true,"spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","excludedProcessImageFileListID":1,"realTimeScan":"read-write","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"networkDirectoriesEnabled":false,"customRemediationActionsEnabled":false,"amsiScanEnabled":true,"scanActionForBehaviorMonitoring":"active-action","scanActionForMachineLearning":"quarantine","ID":4}',
    '{"name":"Default Real-Time Scan Configuration","description":"","scanType":"real-time","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-only","documentExploitHeuristicLevel":"default","machineLearningEnabled":true,"behaviorMonitoringEnabled":true,"documentRecoveryEnabled":false,"intelliTrapEnabled":true,"memoryScanEnabled":false,"spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","excludedDirectoryListID":1,"excludedFileListID":2,"excludedFileExtensionListID":2,"excludedProcessImageFileListID":1,"realTimeScan":"read-write","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"networkDirectoriesEnabled":false,"customRemediationActionsEnabled":false,"amsiScanEnabled":true,"scanActionForBehaviorMonitoring":"pass","scanActionForMachineLearning":"pass","ID":1}',
    '{"name":"Default Manual Scan Configuration","description":"","scanType":"on-demand","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-only","documentExploitHeuristicLevel":"default","spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"customRemediationActionsEnabled":false,"ID":2,"cpuUsage":"high"}',
    '{"name":"Default Scheduled Scan Configuration","description":"","scanType":"on-demand","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-only","documentExploitHeuristicLevel":"default","spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"customRemediationActionsEnabled":false,"ID":3,"cpuUsage":"high"}',
]
mod_allamconfig = [
    '{"name":"Advanced Real-Time Scan Configuration","description":"","scanType":"real-time","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-and-heuristic","documentExploitHeuristicLevel":"default-and-agressive","machineLearningEnabled":true,"behaviorMonitoringEnabled":true,"documentRecoveryEnabled":true,"intelliTrapEnabled":true,"memoryScanEnabled":true,"spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","excludedProcessImageFileListID":160,"realTimeScan":"read-write","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"networkDirectoriesEnabled":false,"customRemediationActionsEnabled":false,"amsiScanEnabled":true,"scanActionForBehaviorMonitoring":"active-action","scanActionForMachineLearning":"quarantine","ID":2}',
    '{"name":"Default Real-Time Scan Configuration","description":"","scanType":"real-time","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-only","documentExploitHeuristicLevel":"default","machineLearningEnabled":true,"behaviorMonitoringEnabled":true,"documentRecoveryEnabled":false,"intelliTrapEnabled":true,"memoryScanEnabled":false,"spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","excludedDirectoryListID":127,"excludedFileListID":161,"excludedFileExtensionListID":89,"excludedProcessImageFileListID":160,"realTimeScan":"read-write","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"networkDirectoriesEnabled":false,"customRemediationActionsEnabled":false,"amsiScanEnabled":true,"scanActionForBehaviorMonitoring":"pass","scanActionForMachineLearning":"pass","ID":1}',
    '{"name":"Default Manual Scan Configuration","description":"","scanType":"on-demand","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-only","documentExploitHeuristicLevel":"default","spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"customRemediationActionsEnabled":false,"ID":2,"cpuUsage":"high"}',
    '{"name":"Default Scheduled Scan Configuration","description":"","scanType":"on-demand","documentExploitProtectionEnabled":true,"documentExploitProtection":"critical-only","documentExploitHeuristicLevel":"default","spywareEnabled":true,"alertEnabled":true,"directoriesToScan":"all-directories","filesToScan":"all-files","scanCompressedEnabled":true,"scanCompressedMaximumSize":2,"scanCompressedMaximumLevels":2,"scanCompressedMaximumFiles":10,"microsoftOfficeEnabled":true,"microsoftOfficeLayers":3,"customRemediationActionsEnabled":false,"ID":3,"cpuUsage":"high"}',
]
