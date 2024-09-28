interface Command {
    val args: List<String>
    val inputStream: IStream
    val outputStream: OStream
    val errorStream: OStream
    fun execute()

    protected fun extractInputStream() : IStream = when(args.size) {
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

    override fun execute() {
        val inputStream = extractInputStream()
        var line: String?
        while (inputStream.readLine().also { line = it } != null) {
            outputStream.writeLine(line!!)
        }
    }
}

class WCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {

    override fun execute() {
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
            charsNumber += line!!.replace(" ", "").toCharArray().size
        }
        val stringResult = when(args.size) {
            0 -> "%6d %6d %6d".format(linesNumber, wordsNumber, charsNumber)
            else -> "%6d %6d %6d %s".format(linesNumber, wordsNumber, charsNumber, args[0])
        }
        outputStream.writeLine(stringResult)
    }
}

class EchoCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute() {
        args.forEach { outputStream.writeLine(it) }
    }
}

class ExitCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {

    override fun execute() {}
}

class PwdCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute() {}
}

class ExternalCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {
    override fun execute() {
        TODO("Not yet implemented")
    }
}

class AssignCommand(
    override val inputStream: IStream,
    override val outputStream: OStream,
    override val errorStream: OStream,
    override val args: List<String>
) : Command {

    override fun execute() {}
}