package org.rhok.h2flow;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONObject;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

public class StatusActivity extends Activity {
	
	private TableLayout				list;		
	private static final String 	SERVER_URI = "http://41.79.111.110:5984/h2mobile/_design/usertap/_view/problemstatus?key=[%22Jabu%22,%22pending%22]";
	private List<String>			problematic_taps;
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.listrow);
        
        //Get Problem Status
        String problems_status = getProblemStatus();
   

		try {
			JSONObject blub = new JSONObject(problems_status);
			JSONArray jsonArray = blub.getJSONArray("rows");
			JSONObject jsonObject = jsonArray.getJSONObject(0);
		    String areaString = (String) jsonObject.getJSONObject("value").get("area");	 
		    final TextView area_view = (TextView) findViewById(R.id.area_name);
			area_view.setText("My Area: "+ areaString);
			
			//Get components
			list =(TableLayout)findViewById(R.id.status_list);
		;	
			for (int i = 0; i < jsonArray.length(); i++) {
				//TableRow itemLayout = (TableRow)LayoutInflater.from(this).inflate(R.layout.listrow, null);
				jsonObject = jsonArray.getJSONObject(i);
				problematic_taps.add((String)jsonObject.getJSONObject("value").get("tapid"));
				
			}
		}catch(Exception e)
		{
			e.printStackTrace();
		}
		
    }
    
    public String getProblemStatus()
    {
    	StringBuilder builder = new StringBuilder();
		HttpClient client = new DefaultHttpClient();
		HttpGet httpGet = new HttpGet(SERVER_URI);
		
		try {
			HttpResponse response = client.execute(httpGet);
			StatusLine statusLine = response.getStatusLine();
			int statusCode = statusLine.getStatusCode();
			
			//is everything OK
			if (statusCode == 200) {
				HttpEntity entity = response.getEntity();
				InputStream content = entity.getContent();
				BufferedReader reader = new BufferedReader(
						new InputStreamReader(content));
				String line;
				while ((line = reader.readLine()) != null) {
					builder.append(line);
				}
			} else {
				Log.e(ReportsActivity .class.toString(), "Failed to get Problem Status");
			}
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		Log.i(ReportsActivity .class.toString(), "JSON Problem Statuses returned: \n" + builder.toString());
		return builder.toString();
    	
    }
}
