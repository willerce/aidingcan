#-*- coding:UTF-8-*-

from canku.config import ProductionConfig

from canku import create_app
app = create_app(config=ProductionConfig())

if __name__ == '__main__':
    app.run()
