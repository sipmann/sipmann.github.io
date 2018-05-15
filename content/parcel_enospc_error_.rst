Parcel ENOSPC error
#############################

:date: 2018-06-05 10:00
:tags: parceljs, enospc, nodejs, inotify
:category: front-end
:slug: parcel_enospc_error
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:description: ENOSPC error when using parcel js on linux
:lang: en
:status: draft

This week I was trying to run a parcel project and for some reason, 
I was getting the message "Error: ENOSPC" from the "watcher" part of Parcel. 
After some research I found that `"listen" project <https://github.com/guard/listen>`_ has a wiki page talking about this kind of problem, related with the inotify, you can read about it `here <https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers#the-technical-details>`_.

The short answer is run the following command on your Linux and be happy.

.. code-block:: shell
  
  echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
