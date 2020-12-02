Title: Scheduling blog posts with Powershell and Pelican
Date: 2099-11-15 07:00
Tags: SQLServer, User, Time Schedule blocking
Category: PowerShell
Slug: schedule-blog-post-with-powershell-and-pelican
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Description: How to schedule posts on pelican using PowerShell and the windows schedule
Lang: en
Status: Draft

Hy folks, first time posting here on dev.to :). Recently I've been migrating some of my scripts from bash to PowerShell and I thought that would be a good time to code an automation script to publish posts on my [personal blog](https://www.sipmann.com). I host my blog with Github Pages and I use [Pelican](http://getpelican.com) as a static site generator. The main problem I have with this toolkit, is the lack of scheduling posts. For those who are new to Pelican, the post system is similar to dev.to, we write the posts using Markdown and we have a `Status` tag to tell when the post is a draft or not. 

The main idea of my script is, run through the Markdown files an check those who have Draft as status. Once I found any post, I start getting some info like the Date and the Slug. The Date part is a little tricky because we need to find the line, split the text and then parse it to do date comparisons. If the post date is lower then the current timespan I replace the `Status: Draft` tag and save the file. After that all we have to do is commit to git and let it go.

```powershell
$postsPath = "E:\projetos\sipmann.github.io\content\";
$files = Get-ChildItem $postsPath -File -Filter *.md

<# Get the current datetime so we can compare with the psot date #>
$now = Get-Date

<# Set the current location, with this we can work with the git commands #>
Set-Location $postsPath

foreach($file in $files) {

	<# Get's only posts with draft status #>
    $isDraft = Get-Content ($postsPath + $file) | Where-Object { $_ -ccontains "Status: Draft" }

    if ($isDraft) {

		<# First we find the line with the date, then we get only the datetime and then parse it #>
        $pubDate = [datetime]::parseexact(((Get-Content ($postsPath + $file) | Where-Object { $_ -Match "^Date:*" }) -split '\s+', 2)[1], 'yyyy-MM-dd HH:mm', $null)

		<# TODO: Maybe call google and bing api to submit a new url #>
		$slug = ((Get-Content ($postsPath + $file) | Where-Object { $_ -Match "^Slug:*" }) -split '\s+', 2)[1]
        
        if ($now -ge $pubDate) {

			<# Sets the content without the Draft status #>
            ((Get-Content ($postsPath + $file)) -replace 'Status: Draft', '') | Set-Content ($postsPath + $file)

            git add .
            git commit -m ("New scheduled post: " + $file)
            git push origin master
        }
    }
}
```

Hope you find the script useful, and if you are interested in the other scripts I'm making with PowerShell, take a look at my [github repo](https://github.com/sipmann/PowerShellScripts), still lacks many of my scripts, but it's there where I'll keep them updated. See ya.