<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=venom&height=150&section=header&text=Narehood&fontSize=48&fontColor=FFFFFF&fontAlignY=40&desc=Michael&descSize=20&descAlignY=68&animation=fadeIn&theme=dark" alt="Narehood" />
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Narehood/Narehood/output/dist/pacman-contribution-graph-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Narehood/Narehood/output/dist/pacman-contribution-graph.svg">
    <img alt="pacman contribution graph" src="https://raw.githubusercontent.com/Narehood/Narehood/output/dist/pacman-contribution-graph.svg">
  </picture>
</p>

### Socials

<p align="left">
  <a href="https://github.com/Narehood" target="_blank" rel="noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github.svg" />
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github.svg" width="32" height="32" alt="GitHub" />
    </picture>
  </a>
  <a href="https://x.com/michaelnarehood" target="_blank" rel="noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/twitter-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/twitter.svg" />
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/twitter.svg" width="32" height="32" alt="X" />
    </picture>
  </a>
  <a href="https://narehood.net" target="_blank" rel="noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/rss-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/rss.svg" />
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/rss.svg" width="32" height="32" alt="Website" />
    </picture>
  </a>
</p>

### GitHub Stats

<p align="left">
  <img height="160" src="https://github-readme-stats.vercel.app/api?username=Narehood&show_icons=true&include_all_commits=true&count_private=true&theme=dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=c9d1d9" alt="Narehood's GitHub stats" />
  <img height="160" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Narehood&layout=compact&theme=dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9" alt="Top languages" />
</p>

### 👷 Check out what I'm currently working on
{{ range recentContributions 5 }}
- [{{ .Repo.Name }}]({{ .Repo.URL }}){{ with .Repo.Description }} - {{ . }}{{ end }}
{{- end }}

### 🌱 My latest projects
{{ range recentRepos 5 }}
- [{{ .Name }}]({{ .URL }}){{ with .Description }} - {{ . }}{{ end }}
{{- end }}

### 🔨 My recent Pull Requests
{{ range recentPullRequests 5 }}
- [{{ .Title }}]({{ .URL }}) on [{{ .Repo.Name }}]({{ .Repo.URL }})
{{- end }}

### ⭐ Recent Stars
{{ range recentStars 5 }}
- [{{ .Repo.Name }}]({{ .Repo.URL }}){{ with .Repo.Description }} - {{ . }}{{ end }}
{{- end }}

### 📫 How to reach me:
- Website : <https://narehood.net>
- Twitter : <https://x.com/michaelnarehood>
- GitHub  : <https://github.com/Narehood>
