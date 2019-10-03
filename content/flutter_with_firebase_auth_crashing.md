Title: Flutter + firebase auth crashing
Date: 2019-10-03 19:00
Tags: flutter, firebase, ArrayMap, NoClassDefFound
Category: Flutter
Slug: flutter_with_firebase_auth_crashing
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com

Hey Folks, recently I've started learning [Flutter](https://flutter.dev/) and right after a TODO List, I tried a Firebase integration. But as soon as I started setting the dependencies, my app stopped opening... just a crash. After a few logs digging, I've found the following log.

```shell
AndroidRuntime: FATAL EXCEPTION: main
AndroidRuntime: Process: com.example.diadocasal, PID: 13672
AndroidRuntime: java.lang.NoClassDefFoundError: Failed resolution of: Landroid/support/v4/util/ArrayMap;
AndroidRuntime: 	at com.google.android.gms.internal.measurement.zzca.<clinit>(Unknown Source:60)
AndroidRuntime: 	at com.google.android.gms.internal.measurement.zzcm.zzr(Unknown Source:7)
AndroidRuntime: 	at com.google.android.gms.measurement.internal.zzfj.<init>(Unknown Source:23)
```

Notice the "NoClassDefFound" of an ArrayMap. To solve that I did the following changes to the files:

```java
//build.gradle file
 ext.kotlin_version = '1.3.20'
[...]
 dependencies {
        classpath 'com.android.tools.build:gradle:3.3.0' // gradle version
```

```ini
;gradle.properties file
org.gradle.jvmargs=-Xmx1536M ;mine have just this line at first
android.useAndroidX=true ; uses androidX instead of the default support library
android.enableJetifier=true ; uses jetpack libraries
android.enableR8=true ; the new code shriker
```

After that, voilà, app up and running.
