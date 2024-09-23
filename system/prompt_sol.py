
async def prepare_sol_prompt(file_path, code_lines, comment_lines, code_to_comment_ratio, rust_code, protocol):
    try:
        SOL_ANALYZER = f''' 
Your task is to analyze the following Rust-based file which is part of a larger program intended for deployment on the Solana blockchain and provide a complexity score to guide manual security audits and formal verification.
    
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
     
2. Evaluate the percentage of commented code, the higher the better.

3. Locate and briefly note the most complex or security-critical functions

4. Assess Solana-specific complexity factors:
   - Use of Program Derived Addresses (PDAs)
   - Implementation of complex account validation logic
   - Handling of multiple signers or complex signer validation
   - Reliance on custom libraries over established ones (e.g., SPL library)
   - Proper handling of account ownership and type checks
   - Correct implementation of rent exemption checks

5. Analyze the code's external dependencies:
   - Note the number and nature of external crates used
   - Note that the use of the Anchor framework makes the code more secure and easier to read and audit. (look for 'use anchor_lang').

6. Consider the number of entry points (e.g., 'pub fn'), the more entry points, the more complex to audit and formally verify the program
   
7. Based on your analysis, assign a complexity score from 1 to 10, where:
- 1-3: Simple Solana program with straightforward and easily reviewed logic
- 4-6: Moderate complexity program with potential security considerations that might complicate the audit
- 7-10: High complexity program with multiple CPIs, multiple instructions and complex account and data structures which are time-consuming to review
</thinking>

Your response must be a JSON file with the following structure:

<output>
{{
  "purpose": "[INSERT BRIEF DESCRIPTION OF THE PROGRAM'S PURPOSE HERE]",
  "complexity": "[INSERT SCORE HERE]",
  "rationale": "[INSERT ONE-SENTENCE EXPLANATION HERE]"
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