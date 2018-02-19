Java - Files.readAllBytes throws OutOfMemory
#############################################

:date: 2018-02-16 21:50
:tags: Java, Files.readAllBytes, outOfMemory
:category: Java
:slug: lendo-files-readAllBytes-outofmemory
:author: Maurício Camargo Sipmann
:email:  sipmann@gmail.com
:linkedin: sipmann
:status: draft

Quando você for interagir com arquivos, surge a possibilidade de "ler" todos os bytes de uma vez só com o `Files.readAllBytes`. Mas preste bem atenção com que tipos de arquivos sua aplicação irá lidar, pois este metodo java possui um limite que está definido como `Integer.MAX_VALUE` como você pode ver abaixo ou nos sources da OpenJDK.

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

Tendo isto em mente, avalie se não é melhor você ler chunks de bytes e trabalhar sob demanda ao invés de carregar todo o arquivo para memória ;). Abaixo um exemplo simples de como pode realizar a leitura por partes.

.. code-block:: java

    byte[] buffer = new byte[1024];
    FileInputStream in = new FileInputStream(file);
    int rc = in.read(buffer);
    while (rc != -1)
    {
        //crazy stuff here with buffer
        rc = in.read(buffer);
    }

