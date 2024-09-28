import org.junit.jupiter.api.Assertions.*
import java.io.File

class WCommandTest {
    @org.junit.jupiter.api.Test
    fun execute() {
        val outputBuffer = StringBuilder()
        val inputFileText = object {}::class.java.getResource("statement.txt").readText()
        val command = WCommand(
            inputFileText.asIStream(),
            outputBuffer.asOStream(),
            StringBuilder().asOStream(),
            listOf()
        )
        command.execute()
        assertEquals("     1    31   185", outputBuffer.toString())
    }
}