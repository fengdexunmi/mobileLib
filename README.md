mobileLib
=========

This project is a mobile library system for 
user.

演示网站：http://book.endselect.com

Android应用：测试中，后期会将源码放到gihub上

项目名称：书童

项目概述：为了方便广大用户从图书馆借书阅读并管理自己的书籍，该项目为用户设计了一整套移动图书管理系统，
          包括了网页端和移动端（Android），并实现数据同步，
          目前所有图书数据均来自豆瓣图书，并没有和图书馆进行合作，所有还没有办法投入到实际使用

网页端功能实现：用户登录、用户注册、在读图书、借书记录、查看图书详情、发表读书笔记

移动端功能实现：用户登录、用户注册、在读图书、借书记录、查看图书详情、查看读书笔记、扫码借书、扫描还书

网页端技术实现：Django（https://www.djangoproject.com/ ）开发; Tastypie（http://http://tastypieapi.org/ ）开发WebService API, 方便移动端获取（GET）、发表（POST）和更新（PATCH）数据

移动端技术实现: 基于Android开发原生应用
