import threading
import Ui

def main():
    thread = threading.Thread(target=Ui.create_gui)
    thread.start()
    thread.join()

if __name__ == '__main__':
    main()
