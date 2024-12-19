import com.xenomachina.argparser.ArgParser
import com.xenomachina.argparser.default

class GrepArgs(parser: ArgParser) {
    val word by parser.flagging("-w", help = "search for full words")

    val caseInsensitive by parser.flagging("-i", help = "case-insensitive search mode")

    val after by parser.storing("-A", help = "number of strings to print after string with a match") { toInt() }
        .default(0)

    val regex by parser.positional("REGEXP", help = "regular expression to find matches with")

    val source by parser.positional("SOURCE", help = "source filename")
        .default("")
}