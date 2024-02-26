from flask import Flask, render_template, request, jsonify
import base64
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addcmd')
def addcmd():
    return render_template('addcmd.html')

@app.route('/write_to_file', methods=['GET'])
def write_to_file():
    val = request.args.get('val')

    if val:
        # Decode the Base64 value
        decoded_val = base64.b64decode(val).decode('utf-8')

        # Write the decoded value to a text file
        with open('parameter_details.txt', 'a') as file:
            file.write(f'{decoded_val}\n')
        return f'Value "{decoded_val}" decoded and written to file successfully!'
    else:
        return 'No value provided in the parameter.'


@app.route('/getfunction')
def get_function():
    try:
        # Read the content of cmd.txt without parsing as JSON
        commands = []
        with open('cmd.txt', 'r') as cmd_file:
            lines = cmd_file.readlines()
            for line in lines:
                commands.append(line.strip())
        commands=commands[0]
        return (commands)
    except FileNotFoundError:
        return 'File not found or empty for cmd.txt.'

    
@app.route('/view_content')
def view_content():
    try:
        # Read the content of the parameter_details.txt file
        with open('parameter_details.txt', 'r') as file:
            content = file.read()
        return render_template('view_content.html', file_content=content)
    except FileNotFoundError:
        return 'File not found or empty.'

@app.route('/add_command', methods=['POST'])
def add_command():
    try:
        command = request.form.get('command')

        if command:
            # Clear the content in the cmd.txt file
            with open('cmd.txt', 'w') as cmd_file:
                cmd_file.write(command + '\n')
            return 'Command added successfully!'
        else:
            return 'No command provided.'
    except Exception as e:
        return f'Error: {str(e)}'


@app.route('/postresult')
def post_result():
    try:
        val = request.args.get('val')

        if val:
            # Ensure correct URL decoding
            val = val.replace(" ", "+")  # Replace spaces with + as they might be URL encoded

            # Decode the Base64 value
            decoded_val = base64.b64decode(val).decode('utf-8')

            # Write the decoded value to a text file (clearing previous content)
            with open('result.txt', 'w') as result_file:
                result_file.write(decoded_val + '\n')

            return f'Value "{decoded_val}" decoded and written to result file successfully!'
        else:
            return 'No value provided in the parameter.'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/getresult')
def get_result():
    try:
        with open('result.txt', 'r') as result_file:
            content = result_file.read()
        return content
    except FileNotFoundError:
        return 'File not found or empty for result.txt.'

if __name__ == '__main__':
    app.run(debug=True)
