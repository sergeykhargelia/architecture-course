class Interpreter {
    private val env = Environment()
    private val lexer = Lexer()
    private val parser = Parser(env)
    private val builder = CommandSequenceBuilder(env)
    private val executor = CommandExecutor()

    fun run() {
        while (true) {
            print("> ")
            val input = readln()
            val tokens = lexer.tokenize(input)
            val commandDescriptions = parser.parseCommands(tokens)
            val commands = builder.buildCommands(commandDescriptions)
            val result = executor.executeCommands(commands)
            if (result.terminate) {
                break
            }
        }
    }
}