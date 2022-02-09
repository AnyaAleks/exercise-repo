#include "coordinatedata.h"
#include "transmissionstructure.h"
#include "marksmodel.h"
#include "unionformodel.h"
#include <QDebug>

#include <QTextStream>
#include <QJsonArray>
#include <QJsonObject>

int CoordinateData::_portClient = 0;
int CoordinateData::_portServer = 0;
//QHostAddress CoordinateData::_hostServer = QHostAddress("127.0.0.1");

CoordinateData::CoordinateData(QObject* parent) : QObject(parent),
    m_someVar("123")//FromQML IIсп
{
    _socket = new QUdpSocket(this);
   // _socket->bind(QHostAddress::Any, m_port);
    _socket->bind(QHostAddress::LocalHost, 1234);
    connect(_socket, SIGNAL(readyRead()), this, SLOT(readyRead()));
    sendClientPorttoServer();

    //bool checkStart = _socket->bind(QHostAddress::LocalHost, m_port); //Any???

//    if(checkStart) /*&& server_status==0*/ //quint16 port = 0//проверка порта
//    {
//        qDebug() << "UDP Server started"<< m_port;
//    }
//    else
//    {
//        qDebug() << "Server couldn't start"<<m_port<<_socket->errorString();
//    }
//    setIsWorked(checkStart);

    ///readyRead();

    /// model is null
   _model=new MarksModel(this);
   ///model exist (not null)
   /// 
   
   //
}

void CoordinateData::anotherFunction()///toQML
{
    qDebug()<< "I am being called x2";
}

QString CoordinateData::someVar()///FromQML IIсп
{
    return m_someVar;
}

void CoordinateData::sendCoordinates(float x, float y) //округление до 4й сотой!
{
    qDebug() << "sendCoordinates from QML " << x << y;
    sendCoordinatestoServer(x, y);

    UFMUnion ufmunion;
    ufmunion.ufm_coordinates.x = x;
    ufmunion.ufm_coordinates.y = y;
}

void CoordinateData::sendColor(int green, int red, int blue, int yellow, int black, int gray)
{
    qDebug() << "sendColor from QML " << green << red << blue << yellow << black << gray;
    sendColorstoServer(green, red, blue, yellow, black, gray);

    UFMUnion ufmunion;
    ufmunion.ufm_color.green = green;
    ufmunion.ufm_color.red = red;
    ufmunion.ufm_color.blue = blue;
    ufmunion.ufm_color.yellow = yellow;
    ufmunion.ufm_color.black = black;
    ufmunion.ufm_color.gray = gray;

    _model->addRecord();
}

void CoordinateData::sendCoordinatestoServer(double x, double y)
{
    TrUnion u_data;

    u_data.d_data.type=1;
    u_data.d_data.x=x;
    u_data.d_data.y=y;

    qDebug() << "data coordinates: " << u_data.d_data.type << u_data.d_data.x << u_data.d_data.y << u_data.bin;

    _socket->writeDatagram(u_data.bin,sizeof (TrStruct),QHostAddress::LocalHost, 1234);
}

void CoordinateData::sendColorstoServer(int green, int red, int blue, int yellow, int black, int gray)
{
    TrUnion u_data;
    u_data.d_data.type = 2;
    u_data.color.green = green;
    u_data.color.red = red;
    u_data.color.blue = blue;
    u_data.color.yellow = yellow;
    u_data.color.black = black;
    u_data.color.gray = gray;

    qDebug() << "data color: " << u_data.color.green << u_data.color.red;

    _socket->writeDatagram(u_data.bin,sizeof (TrStructColor),QHostAddress::LocalHost, 1234);
}

void CoordinateData::sendClientPorttoServer()
{
    TrUnion u_data;
    u_data.d_data.type = 3;
    u_data.port.port = _portClient;

    qDebug() << "data port: " << u_data.port.port;

    _socket->writeDatagram(u_data.bin,sizeof (TrStructPort),QHostAddress::LocalHost, 1234);
}

void CoordinateData::receiveFromQML(char data) ///FromQML
{
    qDebug() << "Call true" << data;

    emit sendToQML();
}

void CoordinateData::readyRead()
{

}

///ToQML
void CoordinateData::callME()
{
    qDebug()<< "I am being called";
}

void CoordinateData::setSomeVar(QString newVar)///FromQML IIсп
{
    if(m_someVar != newVar){
        m_someVar = newVar;
        emit someVarChanged();
    }
}

bool CoordinateData::isWorked() const
{
    return m_isWorked;
}

void CoordinateData::setIsWorked(bool newIsWorked)
{
    if (m_isWorked == newIsWorked)
        return;
    m_isWorked = newIsWorked;
    emit isWorkedChanged();
}

MarksModel *CoordinateData::model() const
{
    return _model;
}
