import com.xenomachina.argparser.ArgParser

class CommandSequenceBuilder(private val env: IEnvironment) {
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

        if (description.type == CommandType.Grep) {
            return try {
                val flags = ArgParser(args.toTypedArray()).parseInto(::GrepArgs)
                GrepCommand(env, inputStream, outputStream, errorStream, args, flags)
            } catch (e: Exception) {
                println("Cannot parse flags for grep command: ${e.message}")
                GrepCommand(env, inputStream, outputStream, errorStream, args, null)
            }
        }

        val commandConstructor = when(description.type) {
            CommandType.Cat -> ::CatCommand
            CommandType.Echo -> ::EchoCommand
            CommandType.WC -> ::WCCommand
            CommandType.PWD -> ::PWDCommand
            CommandType.Exit -> ::ExitCommand
            CommandType.External -> ::ExternalCommand
            CommandType.Assign -> ::AssignCommand
            else -> throw IllegalArgumentException("Unsupported command")
        }

        return commandConstructor(env, inputStream, outputStream, errorStream, args)
    }
}