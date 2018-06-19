package com.company.springprojectbase.controller;

import com.company.springprojectbase.db.models.TestDBObject;
import com.company.springprojectbase.db.service.ITestDbObjectService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
public class TestController {

    @Autowired
    ITestDbObjectService db_service;

    @ResponseBody
    @RequestMapping("/api/")
    String home() {
        return "Hello World!";
    }

    @ResponseBody
    @RequestMapping("/api/health")
    String health() {
        return "UP";
    }

    @ResponseBody
    @RequestMapping("/api/add_random")
    String addRandomObject() {
        TestDBObject obj = new TestDBObject();
        obj.setDescription("something");
        db_service.add(obj);

        return obj.toString();
    }

    @ResponseBody
    @RequestMapping("/api/get/{id}")
    String getById(@PathVariable int id) {
        TestDBObject obj = db_service.getById(id);
        if (obj != null)
            return obj.toString();

        return "";
    }

    @ResponseBody
    @RequestMapping("/api/get/all")
    String getAllDbObjects() {
        List<TestDBObject> test_objects = db_service.getAll();

        StringBuilder sb = new StringBuilder();
        test_objects.forEach(testDBObject -> sb.append(testDBObject.toString()));
        return sb.toString();
    }
}
