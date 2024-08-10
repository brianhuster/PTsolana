package handler

import (
	"github.com/datamonsterr/PTsolana/view"
	// viewCommon "github.com/datamonsterr/PTsolana/view/common"
	"github.com/labstack/echo/v4"
)

func GetIndex(c echo.Context) error {
	return RenderTemplComp(c, view.Index())
}

func GetAboutUs(c echo.Context) error {
	return RenderTemplComp(c, view.AboutUs())
}

func GetContact(c echo.Context) error {
	return RenderTemplComp(c, view.Contact())
}

func GetMembership(c echo.Context) error {
	return RenderTemplComp(c, view.Membership())
}

func GetServices(c echo.Context) error {
	return RenderTemplComp(c, view.Services())
}

func GetManageClass(c echo.Context) error {
	return RenderTemplComp(c, view.ManageClass())
}