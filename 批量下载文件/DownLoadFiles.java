package downLoadFiles;

import java.io.*;
import java.net.URL;
import java.net.URLConnection;

public class DownLoadFiles {
    /**
     * 需要提供一个文件，里面是文件名和url的集合，通过遍历文件，分别进行文件下载和重命名。
     */
    public String resultPath;  //下载文件的存放路径
    public String filePath;  //参数文件的路径，里面是文件名和urls

    public DownLoadFiles(String resultPath, String filePath) {
        this.resultPath = resultPath;
        this.filePath = filePath;
    }

    public void downFiles(String fileURL, String filename) throws IOException {
        //构造URL
        URL weburl = new URL(fileURL);
        //打开链接
        URLConnection connection = weburl.openConnection();
        //设置请求超时时间10s
        connection.setConnectTimeout(10 * 1000);
        //输入流
        InputStream inputStream = connection.getInputStream();

        //数据缓冲区
        byte[] bytes = new byte[1024];
        //读取到的数据长度
        int len;
        //输出文件流
        File file = new File(resultPath);
        if (!file.exists()) {
            file.mkdirs();
        }
        OutputStream outputStream = new FileOutputStream(file.getPath() + "\\" +filename+ ".pdf");
        //开始读取
        while ((len = inputStream.read(bytes)) != -1) {
            outputStream.write(bytes, 0, len);
        }
        //下载完毕，关闭所有链接
        outputStream.close();
        inputStream.close();
    }


    //判断文件编码txt
    public void CharacterCode(String filePath) throws IOException {

        BufferedInputStream bufferedReader = new BufferedInputStream(new FileInputStream(filePath));
        int p = (bufferedReader.read() << 8) + bufferedReader.read();
        String code = null;
        switch (p) {
            case 0xefbb:
                code = "UTF-8";
                break;
            case 0xfffe:
                code = "Unicode";
                break;
            case 0xfeff:
                code = "UTF-16BE";
                break;
            default:
                code = "GBK";
        }
        System.out.println(code);

    }


    public void TakeByTurn(String filePath){
        try {
            InputStreamReader inputStreamReader = new InputStreamReader(new FileInputStream(filePath),"UTF-8");
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            String line = null;
            while((line = bufferedReader.readLine()) != null){
                String[] names = line.split("\t");
                String fileName = names[0];
                String url = names[1];
                this.downFiles(url,fileName);
                System.out.println(fileName+"下载完成！");

            }
            bufferedReader.close();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) throws IOException {
         String resultPath="E:\\download\\files\\";  //下载文件的存放路径
         String filePath = "E:\\download\\files\\urls.txt";  //参数文件的路径，里面是文件名和urls
        DownLoadFiles downLoadFiles = new DownLoadFiles(resultPath,filePath);
        //开始下载文件
        downLoadFiles.TakeByTurn(downLoadFiles.filePath);

    }

}
