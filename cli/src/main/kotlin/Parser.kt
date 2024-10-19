class Parser(private val envReader: EnvironmentReader) {
    fun parseCommands(tokens: List<Token>): List<CommandDescription> {
        if (tokens.isEmpty()) {
            return emptyList()
        }
        val commandDescriptions = mutableListOf<CommandDescription>()
        val builder = CommandDescriptionBuilder()
        for (token in tokens) {
            when (token.type) {
                TokenType.Text -> builder.appendString(token.data)
                TokenType.Variable -> builder.appendString(envReader.getVariable(token.data))
                TokenType.Delimiter -> {
                    builder.flush()
                }
                TokenType.Assign -> {
                    builder.flush()
                    builder.setAssignCommandType()
                }
                TokenType.Pipe -> {
                    builder.getCommand()?.let { commandDescriptions.add(it) }
                }
            }
        }
        builder.getCommand()?.let { commandDescriptions.add(it) }
        return commandDescriptions
    }
}
