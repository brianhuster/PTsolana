package handler

import (
	"context"

	"github.com/a-h/templ"
	"github.com/labstack/echo/v4"
)

func RenderTemplComp(c echo.Context, components templ.Component) error {
	return components.Render(context.Background(), c.Response().Writer)
}
