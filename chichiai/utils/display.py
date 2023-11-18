
from termcolor import cprint
from IPython.display import display, HTML
import sys
import time

# summary colors
COLOR_RESULT_HEADER_NTB = 'blue'
COLOR_RESULT_HEADER_CLI = 'green'
COLOR_RESULT_BODY_CODE = '#555555'
COLOR_RESULT_BODY_TEXT = 'black'

# tool colors
COLOR_TOOL_HEADER = 'magenta'

# error colors
COLOR_ERROR_NTB = '#D86C00'
COLOR_ERROR_CLI = {'color': '\033[31m', 'reset': '\033[0m'}

# user input prompts
COLOR_USR_INPUT_PROMPT = 'blue'
COLOR_USR_INPUT_RANK = 'green'

# token summary colors
COLOR_TOKEN_SUMMARY_HEADER_NTB = 'blue'
COLOR_TOKEN_SUMMARY_TEXT_NTB = 'black'
COLOR_TOKEN_SUMMARY_CLI = 'yellow'


# A wrapper for the print function. This can be used to add additional behaviors or formatting to the print function
def print_wrapper(message, end="\n", flush=False):
    # Add any additional behaviors or formatting here
    formatted_message = message
    print(formatted_message, end=end, flush=flush)


class OutputManager:

    @staticmethod
    def display_results(df=None, answer=None, code=None, rank=None, vector_db=False):
        # Display the results of the analysis
        if 'ipykernel' in sys.modules:
            if df is not None:
                display(HTML(f'<p><b style="color:{COLOR_RESULT_HEADER_NTB};">Here is the head of your dataframe:</b><br><pre style="color:{COLOR_RESULT_BODY_CODE};">{df.head(5)}</pre></p><br>'))
            if answer is not None:
                display(HTML(f'<p><b style="color:{COLOR_RESULT_HEADER_NTB};">I now have the final answer:</b><br><pre style="color:{COLOR_RESULT_BODY_TEXT}; white-space: pre-wrap; font-weight: bold;">{answer}</pre></p><br>'))
            if code is not None:
                display(HTML(f'<p><b style="color:{COLOR_RESULT_HEADER_NTB};">Here is the final code that accomplishes the task:</b><br><pre style="color:{COLOR_RESULT_BODY_CODE};">{code}</pre></p><br>'))
            if vector_db and rank is not None:
                display(HTML(f'<p><b style="color:{COLOR_RESULT_HEADER_NTB};">Solution Rank:</b><br><span style="color:{COLOR_RESULT_BODY_TEXT};">{rank}</span></p><br>'))
        else:
            if df is not None:
                cprint(f"\n>> Here is the head of your dataframe:", COLOR_RESULT_HEADER_CLI, attrs=['bold'])
                print_wrapper(df.head(5))
            if answer is not None:
                cprint(f"\n>> I now have the final answer:\n{answer}", COLOR_RESULT_HEADER_CLI, attrs=['bold'])
            if code is not None:
                cprint(f"\n>> Here is the final code that accomplishes the task:", COLOR_RESULT_HEADER_CLI, attrs=['bold'])
                print_wrapper(code)
            if vector_db and rank is not None:
                cprint(f"\n>> Solution Rank:", COLOR_RESULT_HEADER_CLI, attrs=['bold'])
                print_wrapper(rank)

    @staticmethod
    def display_tool_start(tool, model):
        if tool == 'Planner':
            msg = 'Drafting a plan to provide a comprehensive answer, please wait...'
        elif tool == 'Expert Selector':
            msg = 'Selecting the expert to best answer your query, please wait...'
        elif tool == 'Code Generator':
            msg = 'I am generating the first version of the code, please wait...'
        elif tool == 'Code Debugger':
            msg = 'I am reviewing and debugging the first version of the code to check for any errors, bugs, or inconsistencies and will make corrections if necessary. Please wait...'
        elif tool == 'Code Ranker':
            msg = 'I am going to assess, summarize and rank the answer, please wait...'

        if 'ipykernel' in sys.modules:
            display(HTML(f'<p style="color:{COLOR_TOOL_HEADERK};">\nCalling Model: {model}</p>'))
            display(HTML(f'<p><b style="color:{COLOR_TOOL_HEADER};">{msg}</b></p><br>'))
        else:
            cprint(f"\n>> Calling Model: {model}", COLOR_TOOL_HEADER)
            cprint(f"\n>> {msg}\n", COLOR_TOOL_HEADER, attrs=['bold'])

    @staticmethod
    def display_tool_end(tool):
        if tool == 'Code Debugger':
            msg = 'I have finished debugging the code, and will now proceed to the execution...'
        elif tool == 'Code Generator':
            msg = 'I have finished generating the code, and will now proceed to the execution...'

        if 'ipykernel' in sys.modules:
            display(HTML(f'<p><b style="color:{COLOR_TOOL_HEADER};">{msg}</b></p><br>'))
        else:
            cprint(f"\n>> {msg}\n", COLOR_TOOL_HEADER, attrs=['bold'])

    @staticmethod
    def display_error(error, llm_switch_code = False):
        # Display the error message
        if 'ipykernel' in sys.modules:
            display(HTML(f'<br><b><span style="color:{COLOR_ERROR_NTB};">I ran into an issue:</span></b><br><pre style="color:{COLOR_ERROR_NTB};">{error}</pre><br><b><span style="color:{COLOR_ERROR_NTB};">I will examine it, and try again with an adjusted code.</span></b><br>'))
        else:
            sys.stderr.write(f"{COLOR_ERROR_CLI['color']}>> I ran into an issue: {error}. \n>> I will examine it, and try again with an adjusted code.{COLOR_ERROR_CLI['reset']}\n")
            sys.stderr.flush()

        if llm_switch_code == True:
            if 'ipykernel' in sys.modules:
                display(HTML(f'<span style="color: {COLOR_ERROR_NTB};">Switching model to gpt-4 to try to improve the outcome.</span>'))
            else:
                sys.stderr.write(f"{COLOR_ERROR_CLI['color']}>> Switching model to gpt-4 to try to improve the outcome.{COLOR_ERROR_CLI['reset']}\n")
                sys.stderr.flush()

    @staticmethod
    def display_user_input_prompt():
        # Display the input to enter the prompt
        if 'ipykernel' in sys.modules:
            display(HTML(f'<b style="color:{COLOR_USR_INPUT_PROMPT};">Enter your question or type \'exit\' to quit:</b>'))
            time.sleep(1)
            question = input()
        else:
            cprint("\nEnter your question or type 'exit' to quit:", COLOR_USR_INPUT_PROMPT, attrs=['bold'])
            question = input()

        return question

    @staticmethod
    def display_user_input_rank():
        # Display the input to enter the rank
        if 'ipykernel' in sys.modules:
            display(HTML(f'<b style="color:{COLOR_USR_INPUT_RANK};">Are you happy with the ranking ? If YES type \'yes\'. If NO type in the new rank on a scale from 1-10:</b>'))
            time.sleep(1)
            rank_feedback = input()
        else:
            cprint("\nAre you happy with the ranking ?\nIf YES type 'yes'. If NO type in the new rank on a scale from 1-10:", COLOR_USR_INPUT_RANK, attrs=['bold'])
            rank_feedback = input()

        return rank_feedback

    @staticmethod
    def display_model_switch():
        if 'ipykernel' in sys.modules:
            display(HTML(f'<span style="color:{COLOR_TOOL_HEADER};">Switching model to gpt-4 to debug the code.</span>'))
        else:
            cprint("\n>> Switching model to GPT-4 to debug the code.", COLOR_TOOL_HEADER)

    @staticmethod
    def display_call_summary(summary_text):
        # Display the llm calls summary
        if 'ipykernel' in sys.modules:
            display(HTML(f'''
            <br>
            <p><b style="color:{COLOR_TOKEN_SUMMARY_HEADER_NTB};">Chain Summary (Detailed info in bambooai_consolidated_log.json file):</b></p>
            <pre style="color:{COLOR_TOKEN_SUMMARY_TEXT_NTB}; white-space: pre-line;">{summary_text}</pre>
            '''))
        else:
            cprint("\n>> Chain Summary (Detailed info in bambooai_consolidated_log.json file):", COLOR_TOKEN_SUMMARY_CLI, attrs=['bold'])
            print_wrapper(summary_text)
