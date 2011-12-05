package org.rhok.h2flow;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicHeader;
import org.apache.http.protocol.HTTP;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnFocusChangeListener;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemSelectedListener;

/*Activity for Tap  */
public class ReportsActivity<MyActivity> extends Activity {

	private static String 			username ="Jabu";
	private static final String 	SERVER_URI = "http://41.79.111.110:5984/h2mobile/_design/usertap/_view/usertap?key=%22"+username+"%22";  
	private String 					reports_spinner[] ={"Blocked","Dirty Water","Dripping", "Handle Broken", "Leaking", 
														"Locked","Low Pressure","Missing/Stolen", "No Water", "Water Choking",
														"Vandalized", "Other"};
    private String 					taps_spinner[];
    private EditText 				text_comments;
    private String 					selectedProblematicTap;
    private String					selectedProblemTypeTap;
    private String					problem_comment;
    private EditText 				comments_holder;
    private String					monitoredArea;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.reports_activity);
        comments_holder = (EditText)findViewById(R.id.comments);
        
        //reports spinner
        Spinner s = (Spinner) findViewById(R.id.reports);
        ArrayAdapter adapter = new ArrayAdapter(this,
        android.R.layout.simple_spinner_item, reports_spinner);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item); 
        s.setAdapter(adapter);
        s.setOnItemSelectedListener(new ProblemTypeOnSelectedListener());
        //read monitorProfile from CouchDB
        String userProfile = readMonitorProfile();
   

		try {
			JSONObject blub = new JSONObject(userProfile);
			JSONArray jsonArray = blub.getJSONArray("rows");
			JSONObject jsonObject = jsonArray.getJSONObject(0);
		    String areaString = (String) jsonObject.getJSONObject("value").get("area");
		 
		    final TextView area_view = (TextView) findViewById(R.id.area_view);
			area_view.setText(areaString);
			monitoredArea = areaString;
			
			int size = jsonArray.length();
			taps_spinner = new String[size];	
			for (int i = 0; i < jsonArray.length(); i++) {
				jsonObject = jsonArray.getJSONObject(i);
				taps_spinner[i]=(String)jsonObject.getJSONObject("value").get("tapid");
				}
			
			//taps spinner
	        Spinner t = (Spinner) findViewById(R.id.watertap);
	        ArrayAdapter adapterTaps = new ArrayAdapter(this,
	        android.R.layout.simple_spinner_item, taps_spinner);
	        adapterTaps.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item); 
	        t.setAdapter(adapterTaps);
	        t.setOnItemSelectedListener(new ProblematicTapOnSelectedListener());
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		//add a button Listener
		final Button button = (Button) findViewById(R.id.report_button);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	problem_comment=  comments_holder.getText().toString();
            	if(problem_comment == null)
            	{
            		Toast.makeText(ReportsActivity.this, "comments field empty", Toast.LENGTH_SHORT).show();
            	}
            	else
            	{
            	displayAlert();
            	}
            	
            }
        });
     }
    
    //get monitorProfile 
    public String readMonitorProfile() {
    	
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
				Log.e(ReportsActivity .class.toString(), "Failed to get Monitor Profile");
			}
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		Log.i(ReportsActivity .class.toString(), "JSON monitorProfile returned: \n" + builder.toString());
		return builder.toString();
	}
    
    public String sendMonitorIncident()
    {
        Date curDate = new Date(); 
        String pattern = "yyyy-MM-dd HH:mm:ss";
        SimpleDateFormat formatter = new SimpleDateFormat(pattern);  
        String reportdate = formatter.format(curDate);  
        StringBuilder builder = new StringBuilder();
    	
      	JSONObject object = new JSONObject();
    	try {
    		
    		//package JSON object for sending
    		
    		
    		object.put("username", "Jabu");
    		object.put("status", "pending");
    		object.put("tapid", selectedProblematicTap);
    		object.put("area", monitoredArea);
    		object.put("reportdate", reportdate);
    		object.put("problem", selectedProblemTypeTap);
    		object.put("comments", problem_comment);
    		object.put("type", "comments");	
    		
    		//post JSON object  		
    		String postURL="http://41.79.111.110:5984/h2mobile/";
    		HttpClient client = new DefaultHttpClient();
    		try {
				StringEntity s = new StringEntity(object.toString());
				s.setContentEncoding(new BasicHeader(HTTP.CONTENT_TYPE, "application/json"));
				HttpPost sendJson = new HttpPost(postURL);
	    		sendJson.setEntity(s);
	    		HttpResponse response = client.execute(sendJson);
				StatusLine statusLine = response.getStatusLine();
				int statusCode = statusLine.getStatusCode();
			
				//is everything OK
				if (statusCode == 200 || statusCode == 201) {
					HttpEntity entity = response.getEntity();
					InputStream content = entity.getContent();
					BufferedReader reader = new BufferedReader(
							new InputStreamReader(content));
					String line;
					while ((line = reader.readLine()) != null) {
						builder.append(line);
					}
					Log.i("HTTP_RESPONSE", builder.toString());
					
				} else {
					Log.e(ReportsActivity .class.toString(), "Error: "+statusCode);
				}
	    
	    		
    		} catch (Exception e) {
				e.printStackTrace();
			}		
    		
    	} catch (JSONException e) {
    		e.printStackTrace();
    		Log.i(ReportsActivity .class.toString(), "Failed to send Monitor Incident");
    		return "Error";
    	}
    	return "Problematic Tap Reported";
    }
    
    //this handles sending the logging of the data
	private void completeReporting()
	{
	
	
		//send packaged data
		
		String msg = sendMonitorIncident();
    	if(msg !="Error")
    	{
    	Toast.makeText(ReportsActivity.this, msg, Toast.LENGTH_SHORT).show();
    	text_comments = (EditText)findViewById(R.id.comments);
    	text_comments.setText(""); 

    	}
    	else
    	{
    		Toast.makeText(ReportsActivity.this, "Error ocurred during sending", Toast.LENGTH_SHORT).show();

    	}
		
    	//if(success) finish();
	}
  
    //AlertDialogBox for submission
    public void displayAlert()
    {
 
     AlertDialog.Builder builder = new AlertDialog.Builder(this);
     builder.setMessage("Report the selected tap?")
     		.setTitle("Please Confirm")
            .setCancelable(true)
            .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
             public void onClick(DialogInterface dialog, int id) {
             
            	 //complete sending of data
            	 completeReporting();
             
            }
            })
            .setNegativeButton("No", new DialogInterface.OnClickListener() {
                public void onClick(DialogInterface dialog, int id) {
                     dialog.cancel();
                }
            })
            .show();
    } 
 
    public class ProblematicTapOnSelectedListener implements OnItemSelectedListener {

        public void onItemSelected(AdapterView<?> parent,
            View view, int pos, long id) {
          
        	Toast.makeText(parent.getContext(), "Problematic Tap is " +
            parent.getItemAtPosition(pos).toString(), Toast.LENGTH_LONG).show();      
        	selectedProblematicTap = parent.getItemAtPosition(pos).toString();
          
        }

        public void onNothingSelected(AdapterView parent) {
          // Do nothing.
        }
    }
    
    public class ProblemTypeOnSelectedListener implements OnItemSelectedListener {

        public void onItemSelected(AdapterView<?> parent,
            View view, int pos, long id) {
          
        	Toast.makeText(parent.getContext(), "Problem Type is " +
            parent.getItemAtPosition(pos).toString(), Toast.LENGTH_LONG).show();      
        	selectedProblemTypeTap = parent.getItemAtPosition(pos).toString();
          
        }

        public void onNothingSelected(AdapterView parent) {
          // Do nothing.
        }
    }
}


