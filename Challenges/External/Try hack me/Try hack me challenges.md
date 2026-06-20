```dataviewjs
const challenges = dv.pages("#THMChallenge");

const lastChallengeDate = challenges.sort((a,b) => a.Date > b.Date ).map(file => file.Date)[0]

const date = lastChallengeDate.toFormat("yyyy-MM-dd")

function daysSince(inputDate) {
  const targetDate = new Date(inputDate);
  const today = new Date();

  targetDate.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);

  const diffInMs = today - targetDate;
  const msInDay = 1000 * 60 * 60 * 24;

  return Math.floor(diffInMs / msInDay);
}

const lastChallengeDays = daysSince(date)


dv.span(`
| **STAT** | VAL |
| -------- | --- |
| Challenges logged | **${"`"+challenges.length+"`"}** |
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
- [ ] [Race track bank](https://tryhackme.com/room/racetrackbank) - Hard
- [ ] [Polkit](https://tryhackme.com/room/polkit) - Hard
- [ ] [Fragnista](https://tryhackme.com/room/cve202646300) - Easy
- [ ] [Plant photographer](https://tryhackme.com/room/plantphotographer) - Hard
- [ ] [Crack the hash](https://tryhackme.com/room/crackthehash?vercelChallengeReload=2)- Easy
- [ ] [postX](https://tryhackme.com/room/postexploit)- Easy
- [ ] [Google dorking](https://tryhackme.com/room/googledorking) - Easy
- [ ] [ChrismasCTF](https://tryhackme.com/room/hc0nchristmasctf)