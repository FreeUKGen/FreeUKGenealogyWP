# FreeUKGenealogyWP
For FUG WordPress migration work.

## Fonts
Museo 300 and Museo 500 fonts generated using Fontspring.

Please see the license file for usage of the font files. The "Licensee" in the agreement is "Free UK Genealogy".

### Font Installation Instructions
* font files uploaded by SFTP to fonts folder under the theme folder, so the location is `/wp-content/themes/oceanwp/fonts`
* four font file uploaded:  `Museo300-Regular-webfont.woff`, `Museo300-Regular-webfont.woff2`, `Museo500-Regular-webfont.woff`, `Museo300-Regular-webfont.woff2`
* `stylesheet.css` uploaded to the same fonts folder, this file "installs" the fonts
* the theme `style.css` file modified via Wordpress admin to add the line `<link rel="stylesheet" href="fonts/stylesheet.css" type="text/css" charset="utf-8" />`, which includes the file to install the fonts
