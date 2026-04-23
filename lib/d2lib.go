package main

import (
	"C"

	"context"
	_ "embed"

	cdrslog "cdr.dev/slog"

	"oss.terrastruct.com/d2/d2graph"
	"oss.terrastruct.com/d2/d2layouts/d2elklayout"
	"oss.terrastruct.com/d2/d2lib"
	"oss.terrastruct.com/d2/d2renderers/d2svg"
	"oss.terrastruct.com/d2/d2themes/d2themescatalog"
	d2log "oss.terrastruct.com/d2/lib/log"
	"oss.terrastruct.com/d2/lib/textmeasure"
	"oss.terrastruct.com/util-go/go2"
)

//go:embed adi/adi-theme.d2
var adiThemeLight string

//go:embed adi/adi-theme-dark.d2
var adiThemeDark string

//go:embed adi/adi-components.d2
var adiComponents string

//go:embed sw/sw-theme.d2
var swThemeLight string

//go:embed sw/sw-theme-dark.d2
var swThemeDark string

//go:embed sw/sw-components.d2
var swComponents string

//go:embed jif/jif-theme.d2
var jifThemeLight string

//go:embed jif/jif-theme-dark.d2
var jifThemeDark string

//go:embed jif/jif-components.d2
var jifComponents string

//export runme
func runme(namePtr *C.char) *C.char {

	graph := C.GoString(namePtr)

	ruler, _ := textmeasure.NewRuler()
	layoutResolver := func(engine string) (d2graph.LayoutGraph, error) {
		return d2elklayout.DefaultLayout, nil
	}
	renderOpts := &d2svg.RenderOpts{
		Pad:         go2.Pointer(int64(5)),
		ThemeID:     &d2themescatalog.CoolClassics.ID,
		DarkThemeID: &d2themescatalog.DarkMauve.ID,
	}
	compileOpts := &d2lib.CompileOptions{
		LayoutResolver: layoutResolver,
		Ruler:          ruler,
	}

	ctx := context.Background()
	logger := cdrslog.Make().Leveled(cdrslog.LevelError)
	ctx = d2log.With(ctx, logger)

	diagram, _, err := d2lib.Compile(ctx, graph, compileOpts, renderOpts)
	if err != nil {
		return C.CString("Error compiling D2 diagram: " + err.Error())
	}

	out, err := d2svg.Render(diagram, renderOpts)
	if err != nil {
		return C.CString("Error rendering D2 diagram: " + err.Error())
	}

	outs := string(out)
	return C.CString(outs)
}

//export runmeAdi
func runmeAdi(namePtr *C.char, themeModePtr *C.char) *C.char {
	return runmeLib(namePtr, C.CString("adi"), themeModePtr)
}

//export runmeLib
func runmeLib(codePtr *C.char, libraryPtr *C.char, themeModePtr *C.char) *C.char {
	userCode := C.GoString(codePtr)
	library := C.GoString(libraryPtr)
	themeMode := "light"
	if themeModePtr != nil {
		tm := C.GoString(themeModePtr)
		if tm != "" {
			themeMode = tm
		}
	}

	// Select theme and components based on library name
	var theme, components string
	switch library {
	case "adi":
		if themeMode == "dark" {
			theme = adiThemeDark
		} else {
			theme = adiThemeLight
		}
		components = adiComponents
	case "sw":
		if themeMode == "dark" {
			theme = swThemeDark
		} else {
			theme = swThemeLight
		}
		components = swComponents
	case "jif":
		if themeMode == "dark" {
			theme = jifThemeDark
		} else {
			theme = jifThemeLight
		}
		components = jifComponents
	default:
		return C.CString("Error: unknown library '" + library + "', expected 'adi', 'sw', or 'jif'")
	}

	// Prepend library (components + theme) to user code so theme can
	// override component class styles (needed for dark-mode variants).
	combined := components + "\n" + theme + "\n" + userCode

	ruler, _ := textmeasure.NewRuler()
	layoutResolver := func(engine string) (d2graph.LayoutGraph, error) {
		return d2elklayout.DefaultLayout, nil
	}
	renderOpts := &d2svg.RenderOpts{
		Pad:     go2.Pointer(int64(5)),
		ThemeID: &d2themescatalog.NeutralDefault.ID,
	}
	if themeMode == "dark" {
		renderOpts.DarkThemeID = &d2themescatalog.DarkMauve.ID
	}
	compileOpts := &d2lib.CompileOptions{
		LayoutResolver: layoutResolver,
		Ruler:          ruler,
	}

	ctx := context.Background()
	logger := cdrslog.Make().Leveled(cdrslog.LevelError)
	ctx = d2log.With(ctx, logger)

	diagram, _, err := d2lib.Compile(ctx, combined, compileOpts, renderOpts)
	if err != nil {
		return C.CString("Error compiling D2 diagram: " + err.Error())
	}

	out, err := d2svg.Render(diagram, renderOpts)
	if err != nil {
		return C.CString("Error rendering D2 diagram: " + err.Error())
	}

	return C.CString(string(out))
}

func main() {

}
