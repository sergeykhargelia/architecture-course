import java.io.File

interface IStream {
    fun readLine(): String?
}

fun File.asIStream(): IStream = object : IStream {
    private val lines = this@asIStream.readLines()

    private var idx = 0

    override fun readLine(): String? = lines.getOrNull(idx++)
}