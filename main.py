from ui import Application
import platform

if __name__ == "__main__":
    application = Application(platform.system())
    application.run()
