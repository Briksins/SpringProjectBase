package com.company.springprojectbase;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;

@SpringBootTest
@AutoConfigureMockMvc
@RunWith(SpringRunner.class)
public class SpringProjectBaseApplicationTests {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void contextLoads() {
    }

    @Test
    public void test_RootRequest_helloWorld() throws Exception {
        this.mockMvc.perform(get("/api/"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("Hello World!")));
    }

    @Test
    public void test_health_isUp() throws Exception {
        this.mockMvc.perform(get("/api/health"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("UP")));
    }

    @Test
    public void test_db_addAndGetById() throws Exception {
        this.mockMvc.perform(get("/api/add_random"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("id")));
        this.mockMvc.perform(get("/api/get/1"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("description")));
    }

    @Test
    public void test_db_getAll() throws Exception {
        this.mockMvc.perform(get("/api/get/all"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("id")));
    }
}
