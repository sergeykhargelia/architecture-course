import java.io.File
import java.io.InputStream

interface IStream {
    fun readLine(): String?
}

fun File.asIStream(): IStream = object : IStream {
    private val lines = this@asIStream.readLines()

    private var idx = 0

    override fun readLine(): String? = lines.getOrNull(idx++)
}

fun stdinAsIStream(): IStream = object : IStream {
    override fun readLine(): String? {
        return readLine()
    }
}

fun String.asIStream() : IStream = object : IStream {
    private val lines = this@asIStream.split('\n')

    private var idx = 0

    override fun readLine(): String? = lines.getOrNull(idx++)
}