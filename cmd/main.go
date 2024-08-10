package main

import (
	"log"

	"github.com/datamonsterr/PTsolana/handler"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	e := echo.New()

	e.Use(middleware.Recover())
	e.Use(middleware.LoggerWithConfig(middleware.LoggerConfig{
		Format: "${time_rfc3339} ${method} ${status} ${uri} ${error}\n",
	}))

	e.GET("/", handler.GetIndex)
	e.GET("/index.html", handler.GetIndex)
	e.GET("/about-us.html", handler.GetAboutUs)
	e.GET("/contact.html", handler.GetContact)
	e.GET("/services.html", handler.GetServices)
	e.GET("/manage-class.html", handler.GetManageClass)

	e.Static("/", "static")
	log.Fatal(e.Start(":8080"))
}
