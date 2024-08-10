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
	e.GET("/about-us", handler.GetAboutUs)
	e.GET("/contact", handler.GetContact)
	e.GET("/services", handler.GetServices)
	e.GET("/manage-class", handler.GetManageClass)

	e.Static("/", "static")
	log.Fatal(e.Start(":8080"))
}
