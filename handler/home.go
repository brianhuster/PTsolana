package handler

import (
<<<<<<< HEAD
	"github.com/datamonsterr/PTsolana/view"
=======
	"github.com/datamonsterr/PTSolana/view"
	viewCommon "github.com/datamonsterr/PTSolana/view/common"
>>>>>>> upstream/main
	"github.com/labstack/echo/v4"
)

func GetIndex(c echo.Context) error {
	return RenderTemplComp(c, view.Index())
}

func GetMainView(c echo.Context) error {
	return RenderTemplComp(c, viewCommon.Mainview())
}
