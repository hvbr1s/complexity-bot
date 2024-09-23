async def prepare_sol_prompt_fv(file_path, code_lines, code_to_comment_ratio, rust_code, protocol):
    try:
        SOL_ANALYZER = f''' 
Your task is to analyze the following Rust-based file which is part of a larger program for the {protocol} project and intended for deployment on the Solana blockchain and provide a complexity score to guide its formal verification.
    
Here is the Rust code to analyze:
<rust_code>
{rust_code}
</rust_code>

Here is the metadata for the code:
- Project name: {protocol}
- File name: {file_path}
- Number of lines of code: {code_lines}
- Percentage of commented lines of code: {code_to_comment_ratio}%

Analyze the potential complexity of the program based on the following criteria, think step-by-step:

<thinking>
1. Categorize the program size as:
     * < 100 lines: Very small
     * 100-300 lines: Small
     * 300-500 lines: Medium
     * 500-1000 lines: Large
     * > 1000 lines: Very large
     
2. Assess the percentage of commented code. A higher percentage generally indicates better documentation and may ease formal verification.

3. Count the number of public functions (e.g., pub fn). A higher number of entry points can increase the complexity of formal verification.

4. List functions that are key to the program’s operation and could benefit from formal verification.

5. Evaluate the program's potential challenges for formal verification:
   - Look for presence of floating-point operations (f32 or f64) vs. scaled integers, the presence of floating points make formal verification EXTREMELY difficult.
   - Check for implementation of non-linear mathematical operations (e.g., 'checked_mul', 'checked_div')
   - Identify implementation of complex data structures like Merkle trees, hash tables or binary trees
   - Frequency and complexity of Cross-Program Invocations (CPI) (look for 'invoke' or 'invoke_signed' functions)

6. Assess Solana-specific complexity factors for formal verification:
   - Use of Program Derived Addresses (PDAs)
   - Implementation of complex account validation logic
   - Handling of multiple signers or complex signer validation
   - Reliance on custom libraries over established ones (e.g., SPL library)
   - Proper handling of account ownership and type checks
   - Correct implementation of rent exemption checks

7. Analyze the code's external dependencies:
   - Note the number and nature of external crates used
   - Note that the use of Borsh simplifies serializing and deserializing data structures (look for 'use borsh').
   - Note that the use of Bytemuck simplifies low-level data manipulation (look for 'use bytemuck').
   
8. Based on your analysis, assign a complexity score from 0 to 10, where:
	- 0: Extremely short or simple file, not worth formal verification.
	- 1-3: Simple program with straightforward, easily verifiable logic.
	- 4-6: Moderately complex program with more challenging logic.
	- 7-10: Highly complex program with multiple CPIs, complex account structures, or non-linear mathematics.
</thinking>

Your response must be a JSON file with the following structure:

<output>
{{
  "purpose": "[INSERT BRIEF DESCRIPTION OF THE PROGRAM'S PURPOSE IN THE CONTEXT OF {protocol.capitalize()} HERE]",  
  "complexity": "[INSERT SCORE HERE]",
  "rationale": "[INSERT ONE-SENTENCE EXPLANATION OF THE SCORE HERE]"
}}
</output>

Do not include any additional information or explanations outside of this JSON structure. Ensure that your rationale is concise and directly relates to the assigned complexity score.
        '''
        
        return SOL_ANALYZER
     
    except Exception as e:
        print(e)
        error  = {
            "purpose": "Oops, something went wrong, I wasn't able to score that file!",
            "complexity": "0",
            "rationale": "Oops, something went wrong, I wasn't able to score that file!"
         }
        return error