import org.junit.jupiter.api.Assertions.*
import java.io.File

class CatCommandTest {
    @org.junit.jupiter.api.Test
    fun `test cat with no arguments`() {
        val outputBuffer = StringBuilder()
        val inputFileText = object {}::class.java.getResource("statement.txt").readText()
        val command = CatCommand(
            inputFileText.asIStream(),
            outputBuffer.asOStream(),
            StringBuilder().asOStream(),
            listOf()
        )
        command.execute()
        assertEquals(inputFileText, outputBuffer.toString())
    }

    @org.junit.jupiter.api.Test
    fun `test cat with filename as an argument`() {
        val outputBuffer = StringBuilder()
        val fileName = "statement.txt"
        val resourcesPath = "src\\test\\resources\\"
        val command = CatCommand(
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf(resourcesPath + fileName)
        )
        command.execute()
        val inputFileText = object {}::class.java.getResource(fileName).readText()
        assertEquals(inputFileText, outputBuffer.toString())
    }
}