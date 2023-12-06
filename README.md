# python_zohobooks
Repo of sample code to allow simple Python access to Zoho books api

I have been frustrated by not having any documentation on how to do simple things for the Zoho books API.  Feel free to contact me if you need consulting help for some of this work.

Docs here:
https://www.zoho.com/books/api/v3/introduction/#overview

I see Zoho supports an SDK for many of their products but has not updated any of the Books coding to a current API state.  I spent a little while dusting off my python and zoho books api code pulled together for other projects and came up with this simple sample.  

To use it, you must:
1) Go to the zoho developer console https://api-console.zoho.com/ and create a self client.  Record all details.
2) Place the details from #1 in the source file.
3) Get your organization ID (either from your own Zoho books profile or via this https://www.zoho.com/books/api/v3/introduction/#organization-id - and place this in the org ID in your code.
4) You will find a refresh token from #1.  Place that in the data/refresh_token file.  Do not put anything else in the file.
5) Run the app and it will download your projects and get a sample set of timesheets from the first project in the list.

   
