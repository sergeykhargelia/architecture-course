import org.junit.jupiter.api.Assertions.*
import com.xenomachina.argparser.ArgParser
import org.junit.jupiter.api.Disabled

class GrepCommandTest {
    private val filename = "README.md"

    private fun runTest(args: List<String>, expectedResultString: String) {
        val flags = ArgParser(args.toTypedArray()).parseInto(::GrepArgs)
        val outputBuffer = StringBuilder()
        val command = GrepCommand(
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf(),
            flags
        )
        val executionResult = command.execute()
        assertEquals(0, executionResult.returnCode)
        assertEquals(expectedResultString, outputBuffer.toString())
    }

    @org.junit.jupiter.api.Test
    fun `test grep command with no flags`() {
        runTest(listOf("CLI", filename), "# CLI")
    }


    @org.junit.jupiter.api.Test
    fun `test grep command with -i flag`() {
        runTest(listOf("-i", "Сторонние библиотеки", filename), "## Сторонние библиотеки")
    }

    @org.junit.jupiter.api.Test
    fun `test grep command with -w flag`() {
        runTest(listOf("-w", "CL", filename), "")
        runTest(listOf("-w", "CLI", filename), "# CLI")
    }

    @org.junit.jupiter.api.Test
    fun `test grep command with -A flag`() {
        runTest(listOf("-A", "0", "CLI", filename), "# CLI")
        runTest(listOf("-A", "1", "CLI", filename), "# CLI\n")
        runTest(listOf("-A", "2", "CLI", filename), "# CLI\n\nДанное приложение является простым интерпретатором командной строки, поддерживающим следующие команды:")
    }
}