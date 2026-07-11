```dataviewjs
const daysSince = (inputDate) => {
  const targetDate = new Date(inputDate);
  const today = new Date();

  targetDate.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);

  const diffInMs = today - targetDate;
  const msInDay = 1000 * 60 * 60 * 24;

  return Math.floor(diffInMs / msInDay);
}

function getPagesSortedByDate(source = "", dateField = "file.day", direction = "desc") {
    let pages = dv.pages(source);
    
    const getNestedValue = (p, path) => {
        // Handle Dataview implicit file properties (e.g., file.day, file.ctime)
        if (path.startsWith("file.")) {
            const fileProp = path.split(".")[1];
            return p.file[fileProp];
        }
        // Handle custom frontmatter fields (e.g., metadata.created)
        return path.split('.').reduce((acc, part) => acc && acc[part], p);
    };
    return pages.sort(p => getNestedValue(p, dateField), direction);
}


const print = (str) => {
  dv.span(str)
}

const Challenges = getPagesSortedByDate("#THMChallenge")


const lastChallengeDate = Challenges.map(file => file.Date)[0]
const date = lastChallengeDate.toFormat("yyyy-MM-dd")
const lastChallengeDays = daysSince(date)

// print(Challenges.map(file => file.Date.toFormat("yyyy-MM-dd") + " " + file.file.name))
// dv.span(Challenges.map(file => file.Date.toFormat("yyyy-MM-dd")))

dv.span(`
| **STAT** | VAL |
| -------- | --- |
| Challenges logged | **${"`"+Challenges.length+"`"}** |
| Days since last challenge | **${"`"+lastChallengeDays+"`"}** |
| Date since last challenge | ${lastChallengeDate.toFormat("MMM dd, yyyy (yyyy/MM/dd)")} |
`)
```

# Recent Challenges

```dataviewjs
const challenges = dv.pages("#THMChallenge");

dv.paragraph(`| Challenges |  
| --- |
${challenges.sort(p => p.Date,'desc').map((file) => `| [[${file.file.name}]] | \n`).join("")}` )
```

# Todo
- [ ] Organize Tags
- [ ] Add Tags
	- [ ] Mobile security
	- [ ] Web security
	- [ ] Reverse Engineering
- [ ] Add more sections to Dashboard
- [ ] ...

# Challenges to do
- [x] [Race track bank](https://tryhackme.com/room/racetrackbank) - Hard
- [x] [Plant photographer](https://tryhackme.com/room/plantphotographer) - Hard
- [ ] [Polkit](https://tryhackme.com/room/polkit) - Hard
- [ ] [ChrismasCTF](https://tryhackme.com/room/hc0nchristmasctf) - Hard
- [ ] [Fragnista](https://tryhackme.com/room/cve202646300) - Easy
- [ ] [Crack the hash](https://tryhackme.com/room/crackthehash?vercelChallengeReload=2)- Easy
- [ ] [postX](https://tryhackme.com/room/postexploit)- Easy
- [ ] [Google dorking](https://tryhackme.com/room/googledorking) - Easy
