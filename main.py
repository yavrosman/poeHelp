#import PySimpleGUI as sg
def main():
    layout = [[
        sg.Text('Hello World!'),
        sg.Button('OK')
    ]]
    window = sg.Window('POE Helper Tool', layout)
    while True:
        if sg.window_read(window)[0] == 'EXIT':
            break
        else:
            window.close()

#if __name__ == '__main__':
    main()
