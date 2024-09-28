class CommandExecutor {
    fun executeCommands(commands: List<Command>): ExecutionResult {
        var lastResult = ExecutionResult(0, false)
        for (command in commands) {
            lastResult = command.execute()
            if (lastResult.terminate) {
                break
            }
        }

        return lastResult
    }
}