```dataviewjs
const challenges = dv.pages("#THMChallenge");
// const randomPage = pages[Math.floor(Math.random() * pages.length)];
// dv.paragraph(`> "${randomPage.file.outlinks}" — **${randomPage.file.link}**`);

dv.span(`
| **STAT** | VAL |
| -------- | --- |
| Challenges logged | **${challenges.length}** |
| Date since last challenge | ${challenges.sort((p) => p.file.name, 'desc').map(file => file.Date.toFormat("MMM dd, yyyy (yyyy/MM/dd)") )[0] } |`)
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
- [!] Add more sections to Dashboard
- [ ] ...