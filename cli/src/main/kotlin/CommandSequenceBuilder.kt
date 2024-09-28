class CommandSequenceBuilder(private val envWriter: EnvironmentWriter) {
    fun buildCommands(descriptions: List<CommandDescription>): List<Command> {
        var currentIStream = stdinAsIStream()
        val stdoutStream = stdoutAsOStream()
        val commands: MutableList<Command> = mutableListOf()

        for ((index, d) in descriptions.withIndex()) {
            if (index + 1 < descriptions.size) {
                val currentOStream = Buffer()
                commands.add(buildSingleCommand(d, currentIStream, currentOStream, stdoutStream))
                currentIStream = currentOStream
            } else {
                commands.add(buildSingleCommand(d, currentIStream, stdoutStream, stdoutStream))
            }
        }

        return commands
    }

    private fun buildSingleCommand(
        description: CommandDescription, inputStream: IStream,
        outputStream: OStream, errorStream: OStream
    ): Command {
        val argumentsToDrop = if (description.type == CommandType.External || description.type == CommandType.Assign) 0 else 1
        val args = description.description.drop(argumentsToDrop)

        if (description.type == CommandType.Assign) {
            return AssignCommand(inputStream, outputStream, errorStream, args, envWriter)
        }

        val commandConstructor = when(description.type) {
            CommandType.Cat -> ::CatCommand
            CommandType.Echo -> ::EchoCommand
            CommandType.WC -> ::WCommand
            CommandType.PWD -> ::PwdCommand
            CommandType.Exit -> ::ExitCommand
            CommandType.External -> ::ExternalCommand
            else -> throw IllegalArgumentException("Unsupported command")
        }

        return commandConstructor(inputStream, outputStream, errorStream, args)
    }
}