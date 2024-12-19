import java.nio.file.InvalidPathException
import java.nio.file.Paths
import kotlin.io.path.*
import kotlin.math.min

interface Command {
    val args: List<String>
    val inputStream: IStream
    val outputStream: OStream
    val errorStream: OStream
    val environment: IEnvironment
    fun execute(): ExecutionResult

    fun extractInputStream(): IStream = when (args.size) {
        1 -> environment.currentDirectory.resolve(args[0]).toFile().asIStream()
        0 -> inputStream
        else -> throw IllegalArgumentException("Incorrect number of arguments")
    }
}

class CatCommand(
    override val environment: IEnvironment,
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
    override val environment: IEnvironment,
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
    override val environment: IEnvironment,
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
    override val environment: IEnvironment,
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
    override val environment: IEnvironment,
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        outputStream.writeLine(environment.currentDirectory.toString())
        return ExecutionResult(0, false)
    }
}

class GrepCommand(
    override val environment: IEnvironment,
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>,
    private val flags: GrepArgs?,
) : Command {
    override fun execute(): ExecutionResult {
        if (flags == null) {
            errorStream.writeLine("Failed to parse flags")
            return ExecutionResult(-1, false)
        }

        val file = environment.currentDirectory.resolve(flags.source).toFile()
        if (!file.exists()) {
            errorStream.writeLine("Input file not found")
            return ExecutionResult(-1, false)
        }

        val lines = file.bufferedReader().readLines()
        val regexOptions = if (flags.caseInsensitive) setOf(RegexOption.IGNORE_CASE) else setOf()
        val regex = Regex(flags.regex, regexOptions)

        val suitableLinesIds: MutableList<Int> = mutableListOf()
        lines.forEachIndexed { id, line ->
            if (lineMatches(line, regex, flags.word)) {
                suitableLinesIds.add(id)
            }
        }

        val segmentsToPrint = mergeIds(suitableLinesIds, flags.after)
        segmentsToPrint.forEach { (minIndex, maxIndex) ->
            val rightBorder = min(lines.size - 1, maxIndex + flags.after)
            for (i in minIndex..rightBorder) {
                outputStream.writeLine(lines[i])
            }
        }

        return ExecutionResult(0, false)
    }

    private fun lineMatches(line: String, regex: Regex, matchByWords: Boolean): Boolean {
        if (matchByWords) {
            return line.split(Regex("\\W+")).any { regex.matches(it) }
        }

        return regex.containsMatchIn(line)
    }

    private fun mergeIds(ids: List<Int>, minDistance: Int): List<Pair<Int, Int>> {
        if (ids.isEmpty()) {
            return listOf()
        }

        val result: MutableList<Pair<Int, Int>> = mutableListOf()
        var curLeft = ids.first()
        var curRight = ids.first()

        for (id in ids) {
            if (curLeft + minDistance < id) {
                result.add(Pair(curLeft, curRight))
                curLeft = id
                curRight = id
            } else {
                curRight = id
            }
        }

        result.add(Pair(curLeft, curRight))
        return result
    }
}

class AssignCommand(
    override val environment: IEnvironment,
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>,
) : Command {
    override fun execute(): ExecutionResult {
        return try {
            if (args.size < 2) {
                throw IllegalArgumentException("Cannot execute assign command with less than 2 parameters")
            }
            environment.setVariable(args[0], args[1])
            ExecutionResult(0, false)
        } catch (e: Exception) {
            ExecutionResult(-1, false)
        }
    }
}

class ExternalCommand(
    override val environment: IEnvironment,
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        return try {
            val returnCode = ProcessBuilder(args)
                .directory(environment.currentDirectory.toFile())
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

class CDCommand(
    override val environment: IEnvironment,
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    private val homeDir = System.getProperty("user.home")
    override fun execute(): ExecutionResult {
        environment.currentDirectory = when (args.size) {
            0 -> Paths.get(homeDir).toAbsolutePath()
            1 -> {
                try {
                    environment.currentDirectory.resolve(args[0]).toAbsolutePath()
                } catch (e: InvalidPathException) {
                    errorStream.writeLine("Incorrect path: ${args[0]}")
                    return ExecutionResult(-1, false)
                }
            }
            else -> {
                errorStream.writeLine("Too many arguments for cd")
                return ExecutionResult(-1, false)
            }
        }
        return ExecutionResult(0, false)
    }
}

class LSCommand(
    override val environment: IEnvironment,
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute(): ExecutionResult {
        val path = when (args.size) {
            0 -> environment.currentDirectory
            1 -> environment.currentDirectory.resolve(args[0])
            else -> {
                errorStream.writeLine("Too many arguments for ls")
                return ExecutionResult(-1, false)
            }
        }
        if (path.exists() && path.isDirectory()) {
            path.listDirectoryEntries().forEach {
                outputStream.writeLine(it.name)
            }
            return ExecutionResult(0, false)
        }
        else {
            return ExecutionResult(-1, false)
        }
    }
}
