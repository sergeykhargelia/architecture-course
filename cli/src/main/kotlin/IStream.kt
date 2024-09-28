import java.io.File

interface IStream {
    fun readLine(): String?
}

class MockIStream : IStream {
    override fun readLine(): String? {
        TODO("Not yet implemented")
    }

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