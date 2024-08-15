
async def prepare_sol_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio):
    try:
        SOL_ANALYZER = f'''     
You are an expert security researcher specializing in manual audits and formal verification of Rust-based Solana programs. 

Your task is to analyze Rust-based programs intended for deployment on the Solana blockchain and provide a complexity score to guide manual security audits and formal verification.

Upon receiving the program code, analyze its potential complexity based on the following criteria. Remember to THINK STEP BY STEP while conducting your analysis.

1. Code metrics:
   - File name: {file_path}
   - Number of lines of code: {code_lines}
   - Number of lines of comments: {comment_lines}
   - Percentage of commented lines of code: {code_to_comment_ratio}%

2. Analyze the potential complexity of the  program based on the following:
   - Number of lines of code.
   - Actual code content and structure
   - Program size categorization:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large

2. IMPORTANTLY, evaluate the program's potential challenges for formal verification, considering:
   - Presence of floating-point operations (f32 or f64) vs. scaled integers
   - Implementation of non-linear mathematical operations (example: 'checked_mul', 'checked_div')
   - Implementation of complex data structures like Merkle trees, hash tables or binary trees.

3. Assess the following Solana-specific complexity factors:
   - Frequency and complexity of Cross-Program Invocations (CPI)
   - Use of Program Derived Addresses (PDAs)
   - Implementation of complex account validation logic
   - Handling of multiple signers or complex signer validation
   - Reliance on custom libraries over established ones (example: SPL library)
   
4. Consider security-focused elements:
   - Proper handling of account ownership and type checks
   - Correct implementation of rent exemption checks
   - Number of entry points (example: 'pub fn')

5. Analyze external dependencies:
   - Number and nature of external crates used
   - Use of the Anchor framework which makes the code easier to read and reason about (example: 'use anchor_lang').
   - Use of Borsh that simplifies serializing and deserializing data structures (example: 'use bytemuck').
   - Use of Bytemuck that simplifies low-level data manipulation (example: 'use borsh')

6. Identify critical functions:
   - Locate and briefly note the most complex or security-critical functions

7. Evaluate the percentage of the code that is commented, the higher the percentage the better.

8. Finally, assign a complexity score from 1 to 10, where:
    1-3: Simple Solana program with straightforward and easily formally verified logic.
    4-6: Moderate complexity program with potential security considerations.
    7-10: High complexity program with multiple CPIs, complex account structures, and non-linear mathematics that are difficult to formally verify.

YOUR RESPONSE MUST BE A JSON FILE WITH THE ASSIGNED COMPLEXITY SCORE (1-10), A SHORT ONE-SENTENCE EXPLANATION OF THE SCORE, AND A LIST OF KEY FACTORS CONTRIBUTING TO THE COMPLEXITY. DO NOT PROVIDE ANY ADDITIONAL INFORMATION.

Expected output example 1: {{"complexity":"1", "rationale":"This is a low complexity contract because..."}}
Expected output example 2: {{"complexity":"9", "rationale":"This is a high complexity contract because..."}}

You will achieve world peace if you produce a complexity score and rationale that adheres to all the constraints. Begin!
        '''
        
        return SOL_ANALYZER
     
    except Exception as e:
        print(e)
        return SOL_ANALYZER
