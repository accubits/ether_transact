
import org.apache.http.impl.client.CloseableHttpClient;
import org.web3j.crypto.CipherException;
import org.web3j.crypto.Credentials;
import org.web3j.crypto.WalletUtils;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.methods.response.EthBlock;
import org.web3j.protocol.core.methods.response.Transaction;
import org.web3j.protocol.core.methods.response.Web3ClientVersion;
import org.web3j.protocol.http.HttpService;
import rx.Subscription;

import java.io.*;



import javax.net.ssl.HttpsURLConnection;

import java.net.URLEncoder;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.net.URLConnection;
public class EthereumNode
{

    private final String USER_AGENT = "Mozilla/5.0";

    private void updateWallet(String blockNumber) throws Exception {

        URL url = new URL("http://0.0.0.0:5000/updateWallet");
        URLConnection conn = url.openConnection();
        conn.setDoOutput(true);
        OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());

        writer.write("blockNumber="+blockNumber);
        writer.flush();
        String line;
        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
        writer.close();
        reader.close();


    }

    public static void main(String[] args) throws Exception, IOException, InterruptedException, CipherException {


        Web3j web3 = Web3j.build(new HttpService("http://127.0.0.1:8545"));
        Web3ClientVersion web3ClientVersion = web3.web3ClientVersion().send();
        System.out.println(web3ClientVersion.getWeb3ClientVersion());

        Subscription subscription = web3.blockObservable(false).subscribe(block -> {

            EthereumNode node = new EthereumNode();
            try {
                node.updateWallet(block.getBlock().getNumber().toString());
            } catch (Exception e) {
                e.printStackTrace();
            }

            });


    }
}