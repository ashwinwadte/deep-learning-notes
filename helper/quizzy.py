import json
import random
from pprint import pprint
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.display import display

class Quiz:
    json_file_path = '../helper/quizzes.json'
    def __init__(self, quiz_json_file=json_file_path):
        self.quizzes = self.load_quizzes(quiz_json_file)
    
    def list_quiz(self):
        """
        List all the available quizzes
        @return - prints the list of quizzes
        """
        quiz_list = [{'id': quiz['id'], 'name': quiz['name']} for quiz in self.quizzes]
        pprint(quiz_list)

    def show_quiz(self, id = None, name= None):
        """
        Show the quiz with given id or name
        @return - renders the quiz with submit button
        """
        if id != None:
            query_by, query = 'id', id
        elif name != None:
            query_by, query = 'name', name
        else:
            raise Exception('Provide "id" or "name" to show quiz!')
        
        quiz = self.find_quiz(query_by, query)
        
        options, correct_ans, b_multiple_correct = self.has_multiple_correct(quiz)
        
        self.render_quiz(quiz['question'], options, correct_ans, b_multiple_correct)

    def load_quizzes(self, json_file=None):
        """
        Loads the quizzes json file
        @return - list of quizzes
        """
        with open(json_file) as f:
            data = json.load(f)
        return data['quizzes']
        
    def find_quiz(self, query_by, query):
        for quiz in self.quizzes:
            if query == quiz.get(query_by):
                return quiz
            
    def has_multiple_correct(self, quiz):
        ans = []
        options = []
        for choice in quiz['choices']:
            option, is_correct = list(choice.items())[0]
            options.append(option)
            if is_correct:
                ans.append(option)
        return options, ans, len(ans) > 1
    
    def parse_text_answer(self, correct_ans):
        ans = correct_ans[0].strip()
        ans = ans.split('|')
        return ans
    
    def get_correct_response(self):
        correct_responses = ['Correct!', "That's right!", 'Thanks for completing that!']
        return random.choice(correct_responses)
    
    def render_quiz(self, question, options, correct_ans, b_multiple_correct):
        selected_options = []
        
        # check if text input is needed for this quiz
        b_text_input = len(options) == 1
        
        if b_text_input:
            correct_ans = self.parse_text_answer(correct_ans)
        
        def on_submit(change):
            if b_text_input:
                answer = options_widget.value
                answer = answer.strip()
                del selected_options[:]
                selected_options.append(answer)
            c = set(correct_ans)
            s = set(selected_options)
            if len(s) == 0:
                print('Please choose options!')
            elif s == c:
                print(self.get_correct_response())
            elif s < c:
                if b_text_input:
                    alt = ', '.join(list(c-s))
                    print(f"That's right!\n(Alternatively, {alt} is/are also correct!)")
                else:
                    print(f'{len(s)} out of {len(c)} correct! Keep trying...')
            elif s.isdisjoint(c):
                print('Wrong answer! Please try again.')                
            else:
                print(f'{len(s&c)} out of {len(c)} correct and {len(s-c)} wrong!')
        
        def on_change_checkbox(change):
            checked = change['owner'].value
            text = change['owner'].description
            if checked:
                selected_options.append(text)
            else:
                if len(selected_options) > 0:
                    # initially this list will be empty
                    selected_options.remove(text)
        
        def on_change_radiobutton(change):
            old = change['old']
            new = change['new']
            if len(selected_options) > 0:
                # initially this list will be empty
                selected_options.remove(old)  
            selected_options.append(new)

        layout_style = layout=widgets.Layout(width='80%')
        heading_widget = widgets.HTML(value='<h3><b>Quiz Question</b></h3>')
        question_widget = widgets.HTMLMath(value=f'<b>{question}</b>')
        submit_button_widget = widgets.Button(description='Submit', button_style='info')
        submit_button_widget.on_click(on_submit)
        
        if b_multiple_correct:
            checkboxes = [widgets.Checkbox(value=False, description=option, layout=layout_style) for option in options]
            options_widget = widgets.VBox(checkboxes)
            # add event listener
            for checkbox in checkboxes:
                checkbox.observe(on_change_checkbox, names='value')
        elif b_text_input:
            options_widget = widgets.Text(placeholder='Type your answer')
        else:
            options_widget = widgets.RadioButtons(options=options, value=None, layout=layout_style)
            options_widget.observe(on_change_radiobutton, names='value')
        
        # put the widgets in verticle box holder
        quiz_widget = widgets.VBox([heading_widget, question_widget, options_widget, submit_button_widget])
        
        display(quiz_widget)
        
    def __repr__(self):
        pprint(self.quizzes)
        return ''

def list_quiz():
    """
    API to list all the available quizzes
    @return - prints the list of quizzes
    """
    return Quiz().list_quiz()

def show_quiz(id = None, name= None):
    """
    API to show the quiz with given id or name
    @return - renders the quiz with submit button
    """
    return Quiz().show_quiz(id = id, name= name)
    
def main():
    # pprint(data)
    print('Not implemented yet!')
if __name__ == '__main__':
    main()