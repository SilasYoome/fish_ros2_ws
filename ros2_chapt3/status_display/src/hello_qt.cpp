#include <QApplication>
#include <QLabel>
#include <QString>

int main(int argc, char *argv[]){
    QApplication app(argc,argv);
    QLabel* label = new QLabel();
    QString message = QString::fromStdString("Hello QT!");
    label->setText(message);
    label->show();
    app.exec(); // 執行應用，阻塞程式
    return 0;
}