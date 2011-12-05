package org.rhok.h2flow;

import android.app.TabActivity;
import android.content.Intent;
import android.content.res.Resources;
import android.os.Bundle;
import android.widget.TabHost;

public class H2FlowActivity extends TabActivity {
    
	private TabHost 				tabHost = null;				//Reference to the TabHost View
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        Resources res = getResources(); 	// Resource object to get Drawables
        TabHost tabHost = getTabHost();  	// The activity TabHost
        TabHost.TabSpec spec;  				// Reusable TabSpec for each tab
        Intent intent;  					// Reusable Intent for each tab

        //Create an Intent to launch an Activity for the tab (to be reused)
        intent = new Intent().setClass(this, ReportsActivity.class);

        //Initialize a TabSpec for each tab and add it to the TabHost
        spec = tabHost.newTabSpec("reports").setIndicator("Report Incident",
                          res.getDrawable(R.drawable.tab_report))
                      .setContent(intent);
        tabHost.addTab(spec);

        // Do the same for the other tabs
        intent = new Intent().setClass(this, StatusActivity.class);
        spec = tabHost.newTabSpec("status").setIndicator("View Status",
                          res.getDrawable(R.drawable.tab_status))
                      .setContent(intent);
        tabHost.addTab(spec);

        //set default tab to the details tab
        tabHost.setCurrentTab(0);
    
    }
    
    
}