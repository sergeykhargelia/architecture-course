import java.io.File
import java.nio.file.Paths

interface Command {
    val args: List<String>
    val inputStream: IStream
    val outputStream: OStream
    val errorStream: OStream
    fun execute(): ExecutionResult

    fun extractInputStream() : IStream = when (args.size) {
        1 -> File(args[0]).asIStream()
        0 -> inputStream
        else -> throw IllegalArgumentException("Incorrect number of arguments")
    }
}

class CatCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        return try {
            val inputStream = extractInputStream()
            var line: String?
            while (inputStream.readLine().also { line = it } != null) {
                outputStream.writeLine(line!!)
            }
            ExecutionResult(0, false)
        } catch (e: Exception) {
            ExecutionResult(-1, false)
        }
    }
}

class WCCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        return try {
            val inputStream = extractInputStream()
            var line: String?
            var linesNumber = 0
            var wordsNumber = 0
            var charsNumber = 0
            while (inputStream.readLine().also { line = it } != null) {
                // add 1 to lines number
                linesNumber += 1
                // add number of words to wordsNumber
                wordsNumber += line!!.split(" ").size
                // add number of chars to charsNumber
                charsNumber += line!!.toCharArray().size
            }
            val stringResult = when (args.size) {
                0 -> "%6d%6d%6d".format(linesNumber, wordsNumber, charsNumber)
                else -> "%6d%6d%6d %s".format(linesNumber, wordsNumber, charsNumber, args[0])
            }
            outputStream.writeLine(stringResult)
            ExecutionResult(0, false)
        } catch (e: Exception) {
            ExecutionResult(-1, false)
        }
    }
}

class EchoCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        outputStream.writeLine(args.joinToString(" "))
        return ExecutionResult(0, false)
    }
}

class ExitCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        return ExecutionResult(0, true)
    }
}

class PWDCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        outputStream.writeLine(Paths.get("").toAbsolutePath().toString())
        return ExecutionResult(0, false)
    }
}

class AssignCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>,
    private val envWriter: EnvironmentWriter
) : Command {
    override fun execute(): ExecutionResult {
        return try {
            if (args.size < 2) {
                throw IllegalArgumentException("Cannot execute assign command with less than 2 parameters")
            }
            envWriter.setVariable(args[0], args[1])
            ExecutionResult(0, false)
        } catch (e: Exception) {
            ExecutionResult(-1, false)
        }
    }
}

class ExternalCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        return try {
            val returnCode = ProcessBuilder(args)
                .redirectOutput(ProcessBuilder.Redirect.INHERIT)
                .redirectError(ProcessBuilder.Redirect.INHERIT)
                .start()
                .waitFor()
            ExecutionResult(returnCode, false)
        } catch (e: Exception) {
            ExecutionResult(-1, false)
        }
    }
}