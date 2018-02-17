Java - Files.readAllBytes throws OutOfMemory
##################################

:date: 2018-02-17 13:00
:tags: Java, Files.readAllBytes, outOfMemory
:category: Java
:slug: reading-files-java-readAllBytes-outofmemory
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:language: en


When you need to interact with files, there's the possibility to read all bytes from the file with `Files.readAllBytes`. But be aware of the kinds of files your application will deal with because the Java API files have a limit for the buffer that is defined as `Integer.MAX_VALUE` as you can see above or at the OpenJDK sources.

.. code-block:: java

    public static byte[] readAllBytes(Path path) throws IOException {
        try (FileChannel fc = FileChannel.open(path)) {
            long size = fc.size();
            if (size > (long)Integer.MAX_VALUE)
                throw new OutOfMemoryError("Required array size too large");

            byte[] arr = new byte[(int)size];
            ByteBuffer bb = ByteBuffer.wrap(arr);
            while (bb.hasRemaining()) {
                if (fc.read(bb) < 0) {
                    // truncated
                    break;
                }
            }

            int nread = bb.position();
            return (nread == size) ? arr : Arrays.copyOf(arr, nread);
        }
    }

With that in mind, check if isn't better read chunks of bytes e work with that slice in exchange of loading the whole file into the memory ;). Above a simple example of how you can read chunks of bytes from the file.

.. code-block::java

    byte[] buffer = new byte[1024];
    FileInputStream in = new FileInputStream(file);
    int rc = in.read(buffer);
    while (rc != -1)
    {
        //crazy stuff here with buffer
        rc = in.read(buffer);
    }

