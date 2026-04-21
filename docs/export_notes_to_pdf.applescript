-- Export all Apple Notes from "a course in miracles" folder to PDF
-- Instructions:
-- 1. Open "Script Editor" on your Mac (search for it in Spotlight)
-- 2. Paste this entire script
-- 3. Click the ▶ Run button
-- 4. It will create a folder on your Desktop called "ACIM_Notes_Export"
-- 5. Each note becomes a separate PDF
-- 6. Upload the whole folder (or zip it) to Manus

-- Set the export folder
set exportFolder to (path to desktop as text) & "ACIM_Notes_Export:"

-- Create the folder if it doesn't exist
tell application "Finder"
	if not (exists folder exportFolder) then
		make new folder at desktop with properties {name:"ACIM_Notes_Export"}
	end if
end tell

-- Get the POSIX path for later use
set posixExportFolder to POSIX path of exportFolder

tell application "Notes"
	-- Find the folder - try different possible names
	set targetFolder to missing value
	
	repeat with f in folders
		if name of f is "a course in miracles" or name of f is "A Course in Miracles" or name of f is "ACIM" then
			set targetFolder to f
			exit repeat
		end if
	end repeat
	
	if targetFolder is missing value then
		display dialog "Could not find the ACIM notes folder. Please check the folder name in Apple Notes." buttons {"OK"} default button "OK"
		return
	end if
	
	-- Get all notes in the folder
	set allNotes to notes of targetFolder
	set noteCount to count of allNotes
	
	display dialog "Found " & noteCount & " notes. Starting export..." buttons {"Go!"} default button "Go!"
	
	set exportedCount to 0
	
	repeat with aNote in allNotes
		set noteTitle to name of aNote
		set noteBody to body of aNote
		
		-- Clean the title for use as filename (remove special characters)
		set cleanTitle to my cleanFileName(noteTitle)
		
		-- Create an HTML file first, then convert to PDF via the browser
		set htmlPath to posixExportFolder & cleanTitle & ".html"
		set pdfPath to posixExportFolder & cleanTitle & ".pdf"
		
		-- Build simple HTML with the note content
		set htmlContent to "<!DOCTYPE html><html><head><meta charset='utf-8'><style>body{font-family:-apple-system,Helvetica,Arial,sans-serif;max-width:800px;margin:40px auto;padding:20px;font-size:14px;line-height:1.6;color:#333;}h1{font-size:20px;border-bottom:1px solid #ccc;padding-bottom:10px;}</style></head><body><h1>" & noteTitle & "</h1>" & noteBody & "</body></html>"
		
		-- Write the HTML file
		try
			set fileRef to open for access (POSIX file htmlPath) with write permission
			set eof fileRef to 0
			write htmlContent to fileRef as «class utf8»
			close access fileRef
		on error
			try
				close access fileRef
			end try
		end try
		
		set exportedCount to exportedCount + 1
	end repeat
	
	display dialog "Done! Exported " & exportedCount & " notes as HTML files to ACIM_Notes_Export on your Desktop." & return & return & "Now select all the HTML files, right-click, and choose 'Quick Actions > Create PDF' — or just upload the HTML files directly to Manus." buttons {"Great!"} default button "Great!"
	
end tell

-- Helper function to clean filenames
on cleanFileName(theText)
	set cleanText to ""
	repeat with i from 1 to length of theText
		set c to character i of theText
		if c is in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_" then
			set cleanText to cleanText & c
		end if
	end repeat
	-- Truncate to 50 chars max
	if length of cleanText > 50 then
		set cleanText to text 1 thru 50 of cleanText
	end if
	return cleanText
end cleanFileName
